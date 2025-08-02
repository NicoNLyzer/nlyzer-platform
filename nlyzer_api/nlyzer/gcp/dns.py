"""
DNS Management Module for Tenant Provisioning

This module handles programmatic DNS record creation and management via the
Namecheap API. It follows the Principle of Least Privilege with credentials
stored securely in GCP Secret Manager.

The DNSManager class provides methods to:
- Create DNS A records for tenant subdomains
- Validate DNS propagation
- Manage DNS lifecycle for tenant infrastructure

Security Features:
- Credentials stored in GCP Secret Manager
- Access restricted to provisioning service account
- Comprehensive audit logging
- Error handling with rollback capabilities

Usage:
    dns_manager = DNSManager()
    result = await dns_manager.configure_namecheap_dns_record(
        subdomain="acme-corp",
        ip_address="34.102.136.180"
    )
"""

import asyncio
import logging
import socket
from typing import Dict, Optional, List, Any
from datetime import datetime

from google.cloud import secretmanager
from google.api_core import exceptions as gcp_exceptions

from nlyzer.core.config import settings
from nlyzer.gcp.clients import GCPClientManager
from nlyzer.gcp.exceptions import ProvisioningError

logger = logging.getLogger(__name__)


class DNSConfigurationError(ProvisioningError):
    """Raised when DNS configuration fails."""
    
    def __init__(
        self, 
        message: str,
        subdomain: Optional[str] = None,
        ip_address: Optional[str] = None,
        namecheap_error: Optional[str] = None
    ):
        super().__init__(
            message=f"DNS configuration failed: {message}",
            operation="dns_configuration",
            details={
                "subdomain": subdomain,
                "ip_address": ip_address,
                "namecheap_error": namecheap_error
            }
        )


class DNSManager:
    """
    Manages DNS operations for tenant provisioning via Namecheap API.
    
    This class provides a secure interface to the Namecheap DNS API,
    handling credential management, record creation, and validation.
    All operations are logged for audit compliance.
    
    Attributes:
        _api_client: Namecheap API client instance
        _base_domain: Base domain for tenant subdomains
        _sandbox_mode: Whether to use Namecheap sandbox
    """
    
    def __init__(self, client_manager: Optional[GCPClientManager] = None):
        """
        Initialize the DNS Manager.
        
        Args:
            client_manager: Optional GCP client manager for Secret Manager access
        """
        self._api_client = None
        self._base_domain = settings.NAMECHEAP_BASE_DOMAIN
        self._sandbox_mode = settings.NAMECHEAP_SANDBOX_MODE
        self._client_manager = client_manager or GCPClientManager()
        
        # Initialize the Namecheap client on first use
        self._initialized = False
    
    async def _initialize_client(self) -> None:
        """
        Initialize Namecheap API client with credentials from Secret Manager.
        
        This method retrieves API credentials from GCP Secret Manager and
        initializes the namecheapapi client. Credentials are cached for
        the lifetime of the DNSManager instance.
        
        Raises:
            DNSConfigurationError: If credential retrieval or client init fails
        """
        if self._initialized:
            return
        
        try:
            logger.info("Initializing Namecheap API client")
            
            # Import here to avoid dependency issues if not installed
            try:
                from namecheapapi import DomainAPI
            except ImportError:
                raise DNSConfigurationError(
                    "namecheapapi package not installed. Run: poetry add namecheapapi"
                )
            
            # Retrieve credentials from Secret Manager
            secrets_client = self._client_manager.get_secrets_client()
            
            api_user = await self._get_secret(secrets_client, "namecheap-api-user")
            api_key = await self._get_secret(secrets_client, "namecheap-api-key")
            username = await self._get_secret(secrets_client, "namecheap-username")
            client_ip = await self._get_secret(secrets_client, "namecheap-client-ip")
            
            # Initialize Namecheap client
            self._api_client = DomainAPI(
                api_user=api_user,
                api_key=api_key,
                username=username,
                client_ip=client_ip,
                sandbox=self._sandbox_mode
            )
            
            self._initialized = True
            logger.info(f"Namecheap client initialized (sandbox={self._sandbox_mode})")
            
        except Exception as error:
            error_msg = f"Failed to initialize Namecheap client: {str(error)}"
            logger.error(error_msg)
            raise DNSConfigurationError(error_msg)
    
    async def configure_namecheap_dns_record(
        self, 
        subdomain: str, 
        ip_address: str,
        record_type: str = "A",
        ttl: int = 300
    ) -> Dict[str, Any]:
        """
        Creates a DNS A record for the tenant subdomain.
        
        This method creates a new DNS record in Namecheap for the tenant's
        subdomain, pointing to the Global Load Balancer's static IP address.
        The operation is idempotent - if the record already exists with the
        same IP, it will be updated.
        
        Args:
            subdomain: Tenant subdomain (e.g., "acme-corp")
            ip_address: Static IP of the Global Load Balancer
            record_type: DNS record type (default: "A")
            ttl: Time to live in seconds (default: 300 for quick propagation)
            
        Returns:
            Dict containing:
                - status: "success" or "failed"
                - fqdn: Full domain name created
                - ip_address: The IP address configured
                - ttl: TTL value set
                - created_at: Timestamp of creation
                
        Raises:
            DNSConfigurationError: If DNS record creation fails
        """
        # Ensure client is initialized
        await self._initialize_client()
        
        # Validate inputs
        subdomain = self._sanitize_subdomain(subdomain)
        if not self._validate_ip_address(ip_address):
            raise DNSConfigurationError(
                f"Invalid IP address format: {ip_address}",
                subdomain=subdomain,
                ip_address=ip_address
            )
        
        try:
            fqdn = f"{subdomain}.{self._base_domain}"
            logger.info(
                f"Creating DNS {record_type} record: {fqdn} → {ip_address} (TTL={ttl})"
            )
            
            # Get existing DNS records for the domain
            existing_records = await self._get_existing_records()
            
            # Check if record already exists
            existing_record = self._find_existing_record(
                existing_records, subdomain, record_type
            )
            
            if existing_record:
                if existing_record.get("Address") == ip_address:
                    logger.info(f"DNS record already exists with correct IP: {fqdn}")
                    return {
                        "status": "success",
                        "fqdn": fqdn,
                        "ip_address": ip_address,
                        "ttl": ttl,
                        "created_at": datetime.utcnow().isoformat(),
                        "action": "unchanged"
                    }
                else:
                    logger.info(
                        f"Updating existing DNS record: {fqdn} "
                        f"from {existing_record.get('Address')} to {ip_address}"
                    )
                    # Remove old record
                    existing_records = [
                        r for r in existing_records 
                        if not (r.get("HostName") == subdomain and 
                               r.get("RecordType") == record_type)
                    ]
            
            # Add new record
            new_record = {
                "HostName": subdomain,
                "RecordType": record_type,
                "Address": ip_address,
                "TTL": str(ttl)
            }
            existing_records.append(new_record)
            
            # Update DNS records in Namecheap
            result = await self._set_dns_records(existing_records)
            
            if self._is_operation_successful(result):
                logger.info(f"Successfully configured DNS record for {fqdn}")
                
                return {
                    "status": "success",
                    "fqdn": fqdn,
                    "ip_address": ip_address,
                    "ttl": ttl,
                    "created_at": datetime.utcnow().isoformat(),
                    "action": "updated" if existing_record else "created"
                }
            else:
                error_msg = self._extract_error_message(result)
                raise DNSConfigurationError(
                    f"Namecheap API returned failure",
                    subdomain=subdomain,
                    ip_address=ip_address,
                    namecheap_error=error_msg
                )
                
        except DNSConfigurationError:
            raise
        except Exception as error:
            error_msg = f"Unexpected error during DNS configuration: {str(error)}"
            logger.error(error_msg)
            raise DNSConfigurationError(
                error_msg,
                subdomain=subdomain,
                ip_address=ip_address
            )
    
    async def remove_dns_record(
        self, 
        subdomain: str,
        record_type: str = "A"
    ) -> Dict[str, Any]:
        """
        Removes a DNS record for a tenant subdomain.
        
        This method is used during tenant deprovisioning or rollback
        to clean up DNS records.
        
        Args:
            subdomain: Tenant subdomain to remove
            record_type: DNS record type to remove (default: "A")
            
        Returns:
            Dict with status and details of the removal
        """
        await self._initialize_client()
        subdomain = self._sanitize_subdomain(subdomain)
        
        try:
            fqdn = f"{subdomain}.{self._base_domain}"
            logger.info(f"Removing DNS {record_type} record: {fqdn}")
            
            # Get existing records
            existing_records = await self._get_existing_records()
            
            # Filter out the record to remove
            updated_records = [
                r for r in existing_records
                if not (r.get("HostName") == subdomain and 
                       r.get("RecordType") == record_type)
            ]
            
            if len(updated_records) == len(existing_records):
                logger.info(f"DNS record not found: {fqdn}")
                return {
                    "status": "success",
                    "fqdn": fqdn,
                    "action": "not_found"
                }
            
            # Update DNS records
            result = await self._set_dns_records(updated_records)
            
            if self._is_operation_successful(result):
                logger.info(f"Successfully removed DNS record: {fqdn}")
                return {
                    "status": "success",
                    "fqdn": fqdn,
                    "action": "removed"
                }
            else:
                error_msg = self._extract_error_message(result)
                raise DNSConfigurationError(
                    f"Failed to remove DNS record",
                    subdomain=subdomain,
                    namecheap_error=error_msg
                )
                
        except Exception as error:
            error_msg = f"Failed to remove DNS record: {str(error)}"
            logger.error(error_msg)
            raise DNSConfigurationError(error_msg, subdomain=subdomain)
    
    async def validate_dns_propagation(
        self, 
        fqdn: str, 
        expected_ip: str,
        max_attempts: int = 10,
        delay_seconds: int = 30
    ) -> bool:
        """
        Validates that DNS record has propagated.
        
        This method performs DNS resolution to verify that the newly
        created record is resolvable and returns the expected IP address.
        It will retry with exponential backoff to account for propagation delay.
        
        Args:
            fqdn: Full domain name to check
            expected_ip: Expected IP address
            max_attempts: Maximum number of validation attempts
            delay_seconds: Initial delay between attempts
            
        Returns:
            True if DNS resolves correctly, False otherwise
        """
        logger.info(f"Validating DNS propagation for {fqdn} → {expected_ip}")
        
        for attempt in range(max_attempts):
            try:
                # Perform DNS resolution
                resolved_ips = socket.gethostbyname_ex(fqdn)[2]
                
                if expected_ip in resolved_ips:
                    logger.info(
                        f"DNS validation successful: {fqdn} resolves to {expected_ip}"
                    )
                    return True
                else:
                    logger.warning(
                        f"DNS resolution mismatch (attempt {attempt + 1}): "
                        f"{fqdn} resolves to {resolved_ips}, expected {expected_ip}"
                    )
                    
            except socket.gaierror as error:
                logger.warning(
                    f"DNS resolution failed (attempt {attempt + 1}): "
                    f"{fqdn} - {str(error)}"
                )
            
            # Wait before next attempt (exponential backoff)
            if attempt < max_attempts - 1:
                wait_time = delay_seconds * (2 ** attempt)
                logger.info(f"Waiting {wait_time} seconds before retry...")
                await asyncio.sleep(wait_time)
        
        logger.error(
            f"DNS validation failed after {max_attempts} attempts: "
            f"{fqdn} does not resolve to {expected_ip}"
        )
        return False
    
    # ========================================================================
    # Private Helper Methods
    # ========================================================================
    
    async def _get_secret(
        self, 
        client: secretmanager.SecretManagerServiceClient,
        secret_name: str
    ) -> str:
        """
        Retrieve secret value from GCP Secret Manager.
        
        Args:
            client: Secret Manager client
            secret_name: Name of the secret to retrieve
            
        Returns:
            The secret value as a string
            
        Raises:
            DNSConfigurationError: If secret retrieval fails
        """
        try:
            name = f"projects/{settings.GCP_PROJECT_ID}/secrets/{secret_name}/versions/latest"
            response = client.access_secret_version(request={"name": name})
            return response.payload.data.decode("UTF-8")
        except gcp_exceptions.NotFound:
            raise DNSConfigurationError(
                f"Secret not found in Secret Manager: {secret_name}"
            )
        except Exception as error:
            raise DNSConfigurationError(
                f"Failed to retrieve secret {secret_name}: {str(error)}"
            )
    
    async def _get_existing_records(self) -> List[Dict[str, Any]]:
        """
        Retrieve existing DNS records from Namecheap.
        
        Returns:
            List of existing DNS records
        """
        result = self._api_client.domains_dns_getHosts(self._base_domain)
        return result.get("DomainDNSGetHostsResult", {}).get("host", [])
    
    async def _set_dns_records(self, records: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Update DNS records in Namecheap.
        
        Args:
            records: List of DNS records to set
            
        Returns:
            API response from Namecheap
        """
        return self._api_client.domains_dns_setHosts(self._base_domain, records)
    
    def _sanitize_subdomain(self, subdomain: str) -> str:
        """
        Sanitize and validate subdomain format.
        
        Args:
            subdomain: Raw subdomain input
            
        Returns:
            Sanitized subdomain
            
        Raises:
            DNSConfigurationError: If subdomain is invalid
        """
        # Remove any dots or special characters
        subdomain = subdomain.lower().strip()
        subdomain = "".join(c for c in subdomain if c.isalnum() or c == "-")
        
        # Ensure it doesn't start or end with hyphen
        subdomain = subdomain.strip("-")
        
        # Limit length to DNS standards (63 characters)
        subdomain = subdomain[:63]
        
        if not subdomain:
            raise DNSConfigurationError("Invalid subdomain: empty after sanitization")
        
        return subdomain
    
    def _validate_ip_address(self, ip_address: str) -> bool:
        """
        Validate IP address format.
        
        Args:
            ip_address: IP address to validate
            
        Returns:
            True if valid IPv4 address, False otherwise
        """
        try:
            socket.inet_aton(ip_address)
            return True
        except socket.error:
            return False
    
    def _find_existing_record(
        self, 
        records: List[Dict[str, Any]], 
        subdomain: str, 
        record_type: str
    ) -> Optional[Dict[str, Any]]:
        """
        Find an existing DNS record matching subdomain and type.
        
        Args:
            records: List of existing records
            subdomain: Subdomain to find
            record_type: Record type to match
            
        Returns:
            The matching record dict or None
        """
        for record in records:
            if (record.get("HostName") == subdomain and 
                record.get("RecordType") == record_type):
                return record
        return None
    
    def _is_operation_successful(self, result: Dict[str, Any]) -> bool:
        """
        Check if Namecheap API operation was successful.
        
        Args:
            result: API response from Namecheap
            
        Returns:
            True if successful, False otherwise
        """
        return result.get("DomainDNSSetHostsResult", {}).get("IsSuccess") == "true"
    
    def _extract_error_message(self, result: Dict[str, Any]) -> str:
        """
        Extract error message from Namecheap API response.
        
        Args:
            result: API response from Namecheap
            
        Returns:
            Error message string
        """
        return str(result.get("DomainDNSSetHostsResult", {}).get("Warnings", result))
"""
GCP Client Manager for Centralized Authentication and Client Initialization

This module provides a centralized way to initialize and manage all GCP client
libraries with proper authentication, error handling, and connection pooling.

The GCPClientManager class ensures consistent authentication across all GCP
services and provides a single point of configuration for client settings.

Security Features:
- Application Default Credentials (ADC) for secure authentication
- Client instance caching to prevent authentication overhead
- Centralized credential management
- Error handling for authentication failures

Usage:
    client_manager = GCPClientManager()
    projects_client = client_manager.get_projects_client()
    
    # Client is automatically authenticated and ready to use
    projects = projects_client.list_projects()
"""

import logging
from typing import Optional, Dict, Any

from google.auth import default
from google.auth.credentials import Credentials
from google.cloud import (
    billing_v1,
    compute_v1, 
    iam_admin_v1,
    resourcemanager_v3,
    run_v2,
    secretmanager,
    storage
)
from google.api_core import exceptions as gcp_exceptions

from nlyzer.core.config import settings
from nlyzer.gcp.exceptions import AuthenticationError

logger = logging.getLogger(__name__)


class GCPClientManager:
    """
    Centralized manager for all GCP client libraries.
    
    This class provides a unified interface for initializing and managing
    Google Cloud Platform client libraries. It handles authentication,
    client caching, and provides consistent error handling across all
    GCP services used in tenant provisioning.
    
    Features:
    - Automatic Application Default Credentials (ADC) initialization
    - Client instance caching for performance optimization
    - Centralized error handling and logging
    - Support for all GCP services required for tenant provisioning
    
    Thread Safety:
    This class is thread-safe and can be used across multiple concurrent
    provisioning operations.
    """
    
    def __init__(self, project_id: Optional[str] = None):
        """
        Initialize the GCP Client Manager.
        
        Args:
            project_id: GCP project ID to use as default. If not provided,
                       uses the project ID from settings.
        """
        self._project_id = project_id or settings.GCP_PROJECT_ID
        self._credentials: Optional[Credentials] = None
        self._client_cache: Dict[str, Any] = {}
        
        # Initialize authentication on instantiation
        self._initialize_authentication()
    
    def _initialize_authentication(self) -> None:
        """
        Initialize GCP authentication using Application Default Credentials.
        
        This method attempts to authenticate using the following methods in order:
        1. Service account key file (if GOOGLE_APPLICATION_CREDENTIALS is set)
        2. gcloud user credentials
        3. Metadata service (when running on GCP)
        
        Raises:
            AuthenticationError: If authentication fails
        """
        try:
            self._credentials, detected_project = default()
            
            # Use detected project if none was explicitly provided
            if not self._project_id and detected_project:
                self._project_id = detected_project
            
            logger.info(
                f"GCP authentication initialized successfully for project: {self._project_id}"
            )
            
        except Exception as error:
            error_message = f"Failed to initialize GCP authentication: {str(error)}"
            logger.error(error_message)
            raise AuthenticationError(error_message)
    
    def _get_cached_client(self, client_key: str, client_factory) -> Any:
        """
        Get a cached client instance or create a new one if not cached.
        
        Args:
            client_key: Unique key for caching the client instance
            client_factory: Function that creates the client instance
            
        Returns:
            The client instance
        """
        if client_key not in self._client_cache:
            try:
                self._client_cache[client_key] = client_factory()
                logger.debug(f"Created and cached new {client_key} client")
            except Exception as error:
                error_message = f"Failed to create {client_key} client: {str(error)}"
                logger.error(error_message)
                raise AuthenticationError(error_message, service=client_key)
        
        return self._client_cache[client_key]
    
    # ========================================================================
    # Resource Management Clients
    # ========================================================================
    
    def get_projects_client(self) -> resourcemanager_v3.ProjectsClient:
        """
        Get or create a Resource Manager Projects client.
        
        Used for creating and managing GCP projects during tenant provisioning.
        
        Returns:
            Authenticated ProjectsClient instance
        """
        return self._get_cached_client(
            'projects',
            lambda: resourcemanager_v3.ProjectsClient(credentials=self._credentials)
        )
    
    def get_billing_client(self) -> billing_v1.CloudBillingClient:
        """
        Get or create a Cloud Billing client.
        
        Used for linking billing accounts to newly created tenant projects.
        
        Returns:
            Authenticated CloudBillingClient instance
        """
        return self._get_cached_client(
            'billing',
            lambda: billing_v1.CloudBillingClient(credentials=self._credentials)
        )
    
    # ========================================================================
    # Identity and Access Management Clients
    # ========================================================================
    
    def get_iam_client(self) -> iam_admin_v1.IAMClient:
        """
        Get or create an IAM Admin client.
        
        Used for creating service accounts and managing IAM permissions
        for tenant infrastructure.
        
        Returns:
            Authenticated IAMClient instance
        """
        return self._get_cached_client(
            'iam',
            lambda: iam_admin_v1.IAMClient(credentials=self._credentials)
        )
    
    # ========================================================================
    # Security and Secret Management Clients
    # ========================================================================
    
    def get_secrets_client(self) -> secretmanager.SecretManagerServiceClient:
        """
        Get or create a Secret Manager client.
        
        Used for securely storing tenant API keys, database credentials,
        and other sensitive configuration data.
        
        Returns:
            Authenticated SecretManagerServiceClient instance
        """
        return self._get_cached_client(
            'secrets',
            lambda: secretmanager.SecretManagerServiceClient(credentials=self._credentials)
        )
    
    # ========================================================================
    # Storage Clients
    # ========================================================================
    
    def get_storage_client(self) -> storage.Client:
        """
        Get or create a Cloud Storage client.
        
        Used for creating GCS buckets and storing tenant configuration files
        such as nlweb_config.yml.
        
        Returns:
            Authenticated Cloud Storage Client instance
        """
        return self._get_cached_client(
            'storage',
            lambda: storage.Client(
                credentials=self._credentials,
                project=self._project_id
            )
        )
    
    # ========================================================================
    # Compute Engine Clients
    # ========================================================================
    
    def get_instances_client(self) -> compute_v1.InstancesClient:
        """
        Get or create a Compute Engine Instances client.
        
        Used for creating and managing Weaviate vector database instances
        on Google Compute Engine.
        
        Returns:
            Authenticated InstancesClient instance
        """
        return self._get_cached_client(
            'compute_instances',
            lambda: compute_v1.InstancesClient(credentials=self._credentials)
        )
    
    def get_networks_client(self) -> compute_v1.NetworksClient:
        """
        Get or create a Compute Engine Networks client.
        
        Used for creating and managing VPC networks for tenant isolation.
        
        Returns:
            Authenticated NetworksClient instance
        """
        return self._get_cached_client(
            'compute_networks',
            lambda: compute_v1.NetworksClient(credentials=self._credentials)
        )
    
    def get_firewalls_client(self) -> compute_v1.FirewallsClient:
        """
        Get or create a Compute Engine Firewalls client.
        
        Used for creating firewall rules to secure tenant network traffic.
        
        Returns:
            Authenticated FirewallsClient instance
        """
        return self._get_cached_client(
            'compute_firewalls',
            lambda: compute_v1.FirewallsClient(credentials=self._credentials)
        )
    
    def get_operations_client(self) -> compute_v1.GlobalOperationsClient:
        """
        Get or create a Compute Engine Global Operations client.
        
        Used for monitoring long-running operations during resource creation.
        
        Returns:
            Authenticated GlobalOperationsClient instance
        """
        return self._get_cached_client(
            'compute_operations',
            lambda: compute_v1.GlobalOperationsClient(credentials=self._credentials)
        )
    
    # ========================================================================
    # Cloud Run Clients
    # ========================================================================
    
    def get_run_services_client(self) -> run_v2.ServicesClient:
        """
        Get or create a Cloud Run Services client.
        
        Used for deploying NLWeb engine containers as Cloud Run services
        for each tenant.
        
        Returns:
            Authenticated ServicesClient instance
        """
        return self._get_cached_client(
            'run_services',
            lambda: run_v2.ServicesClient(credentials=self._credentials)
        )
    
    # ========================================================================
    # Utility Methods
    # ========================================================================
    
    def get_project_id(self) -> str:
        """
        Get the current project ID.
        
        Returns:
            The GCP project ID being used by this client manager
        """
        return self._project_id
    
    def get_credentials(self) -> Credentials:
        """
        Get the current credentials.
        
        Returns:
            The authenticated credentials being used by this client manager
        """
        return self._credentials
    
    def clear_cache(self) -> None:
        """
        Clear all cached client instances.
        
        This forces recreation of all clients on next access, which can be
        useful if credentials have been refreshed or if there are connection
        issues.
        """
        self._client_cache.clear()
        logger.info("Cleared all cached GCP client instances")
    
    def get_cache_info(self) -> Dict[str, bool]:
        """
        Get information about cached clients.
        
        Returns:
            Dictionary mapping client names to whether they are cached
        """
        return {
            client_key: client_key in self._client_cache
            for client_key in [
                'projects', 'billing', 'iam', 'secrets', 'storage',
                'compute_instances', 'compute_networks', 'compute_firewalls',
                'compute_operations', 'run_services'
            ]
        }
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit - clear cache on exit."""
        self.clear_cache()
        return False
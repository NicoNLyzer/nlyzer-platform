"""
Custom exceptions for GCP provisioning operations.

This module defines all custom exception classes used throughout the GCP
integration module, providing clear error categories and detailed error
information for debugging and monitoring.
"""

from typing import Optional, Dict, Any


class ProvisioningError(Exception):
    """
    Base exception for all provisioning-related errors.
    
    This is the parent class for all GCP provisioning errors, providing
    common functionality for error tracking and debugging.
    
    Attributes:
        message: Human-readable error description
        tenant_id: ID of the tenant being provisioned (if applicable)
        project_id: GCP project ID involved in the error (if applicable)
        operation: The specific operation that failed
        details: Additional error context and debugging information
    """
    
    def __init__(
        self, 
        message: str,
        tenant_id: Optional[str] = None,
        project_id: Optional[str] = None,
        operation: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(message)
        self.message = message
        self.tenant_id = tenant_id
        self.project_id = project_id
        self.operation = operation
        self.details = details or {}
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert exception to dictionary for JSON serialization."""
        return {
            "error_type": self.__class__.__name__,
            "message": self.message,
            "tenant_id": self.tenant_id,
            "project_id": self.project_id,
            "operation": self.operation,
            "details": self.details
        }


class TenantAlreadyExistsError(ProvisioningError):
    """
    Raised when attempting to provision a tenant that already exists.
    
    This error occurs when trying to create infrastructure for a tenant_id
    that has already been provisioned, preventing duplicate resource creation
    and billing conflicts.
    """
    
    def __init__(self, tenant_id: str, existing_project_id: Optional[str] = None):
        message = f"Tenant {tenant_id} already has provisioned infrastructure"
        if existing_project_id:
            message += f" in project {existing_project_id}"
        
        super().__init__(
            message=message,
            tenant_id=tenant_id,
            project_id=existing_project_id,
            operation="tenant_provisioning"
        )


class ResourceCreationError(ProvisioningError):
    """
    Raised when GCP resource creation fails.
    
    This error occurs when any GCP resource (project, compute instance, 
    Cloud Run service, etc.) fails to be created during the provisioning
    process.
    """
    
    def __init__(
        self, 
        resource_type: str,
        message: str,
        tenant_id: Optional[str] = None,
        project_id: Optional[str] = None,
        gcp_error: Optional[Exception] = None
    ):
        full_message = f"Failed to create {resource_type}: {message}"
        
        details = {"resource_type": resource_type}
        if gcp_error:
            details["gcp_error"] = str(gcp_error)
            details["gcp_error_type"] = type(gcp_error).__name__
        
        super().__init__(
            message=full_message,
            tenant_id=tenant_id,
            project_id=project_id,
            operation=f"create_{resource_type}",
            details=details
        )


class AuthenticationError(ProvisioningError):
    """
    Raised when GCP authentication fails.
    
    This error occurs when the provisioning service cannot authenticate
    with Google Cloud Platform APIs, typically due to credential issues
    or insufficient permissions.
    """
    
    def __init__(self, message: str, service: Optional[str] = None):
        full_message = f"GCP authentication failed: {message}"
        if service:
            full_message += f" for service {service}"
        
        super().__init__(
            message=full_message,
            operation="authentication",
            details={"service": service} if service else {}
        )


class NetworkingError(ProvisioningError):
    """
    Raised when VPC network or firewall configuration fails.
    
    This error occurs during the networking setup phase of tenant
    provisioning, including VPC creation, subnet configuration,
    and firewall rule setup.
    """
    
    def __init__(
        self, 
        message: str,
        tenant_id: Optional[str] = None,
        project_id: Optional[str] = None,
        network_resource: Optional[str] = None
    ):
        super().__init__(
            message=f"Networking configuration failed: {message}",
            tenant_id=tenant_id,
            project_id=project_id,
            operation="networking_setup",
            details={"network_resource": network_resource} if network_resource else {}
        )


class DeploymentValidationError(ProvisioningError):
    """
    Raised when deployed services fail health checks or validation.
    
    This error occurs during the final validation phase when deployed
    NLWeb or Weaviate services are not responding correctly or fail
    their health checks.
    """
    
    def __init__(
        self, 
        service_name: str,
        message: str,
        tenant_id: Optional[str] = None,
        project_id: Optional[str] = None,
        endpoint_url: Optional[str] = None
    ):
        super().__init__(
            message=f"Service validation failed for {service_name}: {message}",
            tenant_id=tenant_id,
            project_id=project_id,
            operation="deployment_validation",
            details={
                "service_name": service_name,
                "endpoint_url": endpoint_url
            }
        )


class CleanupError(ProvisioningError):
    """
    Raised when cleanup of failed provisioning resources fails.
    
    This error occurs when the system attempts to clean up partially
    created resources after a provisioning failure, but the cleanup
    itself encounters errors.
    """
    
    def __init__(
        self, 
        message: str,
        tenant_id: Optional[str] = None,
        project_id: Optional[str] = None,
        failed_resources: Optional[list] = None
    ):
        super().__init__(
            message=f"Resource cleanup failed: {message}",
            tenant_id=tenant_id,
            project_id=project_id,
            operation="cleanup",
            details={"failed_resources": failed_resources or []}
        )
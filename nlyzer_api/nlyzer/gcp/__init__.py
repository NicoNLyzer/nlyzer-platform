"""
GCP Integration Module for NLyzer Platform

This module provides all Google Cloud Platform integrations for the NLyzer platform,
including automated tenant provisioning, resource management, and infrastructure
orchestration.

Key Components:
- provisioning: Automated tenant infrastructure deployment
- clients: Centralized GCP client management and authentication
- exceptions: Custom exception classes for GCP operations

Security Requirements:
- All operations follow principle of least privilege
- Complete tenant isolation at GCP project level
- Comprehensive audit logging for compliance
- Secure credential management via Secret Manager

Usage:
    from nlyzer.gcp.provisioning import provision_new_tenant
    
    result = await provision_new_tenant(tenant_id, config)
"""

from nlyzer.gcp.provisioning import provision_new_tenant
from nlyzer.gcp.clients import GCPClientManager
from nlyzer.gcp.exceptions import (
    ProvisioningError,
    TenantAlreadyExistsError,
    ResourceCreationError,
    AuthenticationError
)

__all__ = [
    'provision_new_tenant',
    'GCPClientManager', 
    'ProvisioningError',
    'TenantAlreadyExistsError',
    'ResourceCreationError',
    'AuthenticationError'
]

__version__ = '1.0.0'
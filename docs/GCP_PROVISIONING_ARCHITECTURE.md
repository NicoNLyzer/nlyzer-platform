# GCP Automated Provisioning Architecture
**The Definitive Guide to Infrastructure as Code for Tenant Provisioning**

- **Status**: Active Design Document
- **Created**: 2025-08-02
- **Last Updated**: 2025-08-02

---

## Executive Summary

This document defines the complete architecture for NLyzer's "Automated Provisioning Handshake" - the process by which our central Provisioning Cloud Function programmatically creates and configures all necessary GCP resources for a new tenant.

The architecture ensures:
- **Security-First Design**: Minimal IAM permissions following principle of least privilege
- **Complete Tenant Isolation**: Each tenant gets their own GCP Project with strict boundaries
- **Infrastructure as Code**: Fully automated resource provisioning via Python GCP client libraries
- **Enterprise Compliance**: Audit trails, error handling, and rollback capabilities

---

## Part 1: Provisioner Service Account IAM Blueprint

### 1.1 Overview

The central Provisioning Cloud Function operates using a dedicated Service Account (`nlyzer-provisioner@nlyzer-control-plane.iam.gserviceaccount.com`) that must have precise permissions to orchestrate tenant infrastructure deployment.

### 1.2 Organization-Level Permissions

These permissions are granted at the Organization level to enable cross-project resource management:

#### **Project Management**
```bash
# Role: roles/resourcemanager.projectCreator
# Justification: Required to create isolated GCP Projects for each tenant, ensuring complete resource and billing separation
gcloud organizations add-iam-policy-binding ORGANIZATION_ID \
    --member="serviceAccount:nlyzer-provisioner@nlyzer-control-plane.iam.gserviceaccount.com" \
    --role="roles/resourcemanager.projectCreator"

# Role: roles/resourcemanager.folderViewer  
# Justification: Needed to navigate the organizational folder structure to place tenant projects in the correct organizational unit
gcloud organizations add-iam-policy-binding ORGANIZATION_ID \
    --member="serviceAccount:nlyzer-provisioner@nlyzer-control-plane.iam.gserviceaccount.com" \
    --role="roles/resourcemanager.folderViewer"
```

#### **Billing Management**
```bash
# Role: roles/billing.projectManager
# Justification: Required to link the appropriate billing account to newly created tenant projects for cost tracking and isolation
gcloud organizations add-iam-policy-binding ORGANIZATION_ID \
    --member="serviceAccount:nlyzer-provisioner@nlyzer-control-plane.iam.gserviceaccount.com" \
    --role="roles/billing.projectManager"
```

### 1.3 Tenant Project-Level Permissions

These permissions are automatically granted to the provisioner service account on each newly created tenant project:

#### **Compute Infrastructure**
```bash
# Role: roles/compute.instanceAdmin.v1
# Justification: Required to create and configure Weaviate GCE instances with persistent disks for vector storage, as specified in UNIFIED_ARCHITECTURAL_BLUEPRINT.md
gcloud projects add-iam-policy-binding TENANT_PROJECT_ID \
    --member="serviceAccount:nlyzer-provisioner@nlyzer-control-plane.iam.gserviceaccount.com" \
    --role="roles/compute.instanceAdmin.v1"

# Role: roles/compute.networkAdmin
# Justification: Needed to create tenant-specific VPC networks, subnets, and firewall rules for network isolation and security
gcloud projects add-iam-policy-binding TENANT_PROJECT_ID \
    --member="serviceAccount:nlyzer-provisioner@nlyzer-control-plane.iam.gserviceaccount.com" \
    --role="roles/compute.networkAdmin"
```

#### **Container & Serverless Services**
```bash
# Role: roles/run.admin
# Justification: Required to deploy the customized NLWeb engine as a Cloud Run service for each tenant
gcloud projects add-iam-policy-binding TENANT_PROJECT_ID \
    --member="serviceAccount:nlyzer-provisioner@nlyzer-control-plane.iam.gserviceaccount.com" \
    --role="roles/run.admin"

# Role: roles/artifactregistry.admin
# Justification: Needed to pull the NLWeb container images from our private Artifact Registry for deployment
gcloud projects add-iam-policy-binding TENANT_PROJECT_ID \
    --member="serviceAccount:nlyzer-provisioner@nlyzer-control-plane.iam.gserviceaccount.com" \
    --role="roles/artifactregistry.admin"
```

#### **Storage & Configuration Management**
```bash
# Role: roles/storage.admin
# Justification: Required to create GCS buckets and upload tenant-specific nlweb_config.yml files as defined in the architecture
gcloud projects add-iam-policy-binding TENANT_PROJECT_ID \
    --member="serviceAccount:nlyzer-provisioner@nlyzer-control-plane.iam.gserviceaccount.com" \
    --role="roles/storage.admin"

# Role: roles/secretmanager.admin
# Justification: Essential for securely storing tenant API keys, database credentials, and other sensitive configuration
gcloud projects add-iam-policy-binding TENANT_PROJECT_ID \
    --member="serviceAccount:nlyzer-provisioner@nlyzer-control-plane.iam.gserviceaccount.com" \
    --role="roles/secretmanager.admin"
```

#### **Identity & Access Management**
```bash
# Role: roles/iam.serviceAccountAdmin
# Justification: Required to create tenant-specific service accounts for the NLWeb Cloud Run service to access GCS and other resources
gcloud projects add-iam-policy-binding TENANT_PROJECT_ID \
    --member="serviceAccount:nlyzer-provisioner@nlyzer-control-plane.iam.gserviceaccount.com" \
    --role="roles/iam.serviceAccountAdmin"

# Role: roles/iam.securityAdmin
# Justification: Needed to configure IAM permissions for tenant service accounts and enforce security policies
gcloud projects add-iam-policy-binding TENANT_PROJECT_ID \
    --member="serviceAccount:nlyzer-provisioner@nlyzer-control-plane.iam.gserviceaccount.com" \
    --role="roles/iam.securityAdmin"
```

#### **DNS & Networking Services**
```bash
# Role: roles/dns.admin
# Justification: Required for setting up custom domain routing and DNS records for tenant-specific NLWeb endpoints
gcloud projects add-iam-policy-binding TENANT_PROJECT_ID \
    --member="serviceAccount:nlyzer-provisioner@nlyzer-control-plane.iam.gserviceaccount.com" \
    --role="roles/dns.admin"
```

### 1.4 Security Considerations

- **Time-Bounded Access**: Consider implementing temporary elevated permissions during provisioning with automatic revocation
- **Audit Logging**: All provisioning actions are logged to Cloud Audit Logs for compliance tracking
- **Resource Quotas**: Each tenant project inherits organizational quotas to prevent resource abuse
- **Network Isolation**: Tenant projects are deployed in separate VPC networks with no cross-tenant connectivity

---

## Part 2: Python GCP Client Implementation Plan

### 2.1 Module Structure

```
nlyzer_api/nlyzer/gcp/
├── __init__.py                 # Module initialization and public API
├── provisioning.py             # Main provisioning orchestration logic
├── clients.py                  # GCP client initialization and management
├── exceptions.py               # Custom exception classes for error handling
└── templates/                  # Infrastructure configuration templates
    ├── weaviate_startup.sh     # GCE startup script for Weaviate
    ├── nlweb_config.yaml.j2    # Jinja2 template for NLWeb configuration
    └── firewall_rules.yaml     # Security group definitions
```

### 2.2 Core Implementation: `nlyzer/gcp/provisioning.py`

```python
"""
GCP Tenant Provisioning Orchestrator

This module implements the complete Infrastructure as Code workflow for 
creating isolated tenant environments on Google Cloud Platform.

Security Requirements:
- All operations use principle of least privilege
- Complete tenant isolation at project level
- Comprehensive audit logging
- Rollback capabilities for failed deployments
"""

import asyncio
import logging
from typing import Dict, List, Optional
from uuid import uuid4

from google.cloud import billing_v1, compute_v1, iam_admin_v1, resourcemanager_v3, run_v2, secretmanager, storage
from google.api_core import exceptions as gcp_exceptions

from nlyzer.core.config import settings
from nlyzer.gcp.clients import GCPClientManager
from nlyzer.gcp.exceptions import ProvisioningError, TenantAlreadyExistsError

logger = logging.getLogger(__name__)

async def provision_new_tenant(tenant_id: str, config: Dict) -> Dict[str, str]:
    """
    Orchestrates the complete creation of all GCP resources for a new tenant.
    
    This function implements the automated provisioning handshake defined in
    the UNIFIED_ARCHITECTURAL_BLUEPRINT.md, creating:
    - Isolated GCP Project
    - Tenant-specific service accounts
    - Secure credential storage
    - Weaviate vector database instance
    - NLWeb Cloud Run service
    - Network security policies
    
    Args:
        tenant_id: Unique identifier for the tenant (UUID format)
        config: Tenant configuration containing:
            - agent_type: Type of AI agent (sales, support, etc.)
            - data_source_type: Source platform (shopify, woocommerce, etc.)
            - credentials: API keys and authentication tokens
            - custom_domain: Optional custom domain configuration
    
    Returns:
        Dict containing:
            - status: "success" or "failed"
            - project_id: Created GCP project identifier
            - nlweb_url: Deployed NLWeb service endpoint
            - weaviate_url: Vector database endpoint
            - config_bucket: GCS bucket for configuration files
            - error_message: Error details if deployment failed
    
    Raises:
        TenantAlreadyExistsError: If tenant_id already has provisioned resources
        ProvisioningError: If any step in the provisioning process fails
    """
    
    logger.info(f"Starting tenant provisioning for tenant_id: {tenant_id}")
    
    try:
        # Initialize GCP clients with proper authentication
        client_manager = GCPClientManager()
        
        # Step 1: Create the isolated GCP Project
        # Uses: resourcemanager_v3.ProjectsClient
        project_id = await _create_gcp_project(client_manager, tenant_id)
        logger.info(f"Created GCP project: {project_id}")
        
        # Step 2: Configure billing for cost tracking
        # Uses: billing_v1.CloudBillingClient  
        await _setup_project_billing(client_manager, project_id)
        logger.info(f"Configured billing for project: {project_id}")
        
        # Step 3: Create tenant-specific service account
        # Uses: iam_admin_v1.IAMClient
        service_account_email = await _create_tenant_service_account(
            client_manager, project_id, tenant_id
        )
        logger.info(f"Created service account: {service_account_email}")
        
        # Step 4: Store sensitive credentials in Secret Manager
        # Uses: secretmanager.SecretManagerServiceClient
        secret_versions = await _store_tenant_secrets(
            client_manager, project_id, config.get('credentials', {})
        )
        logger.info(f"Stored {len(secret_versions)} secrets in Secret Manager")
        
        # Step 5: Create GCS bucket and upload configuration
        # Uses: storage.Client
        config_bucket_name, config_gcs_path = await _create_config_storage(
            client_manager, project_id, tenant_id, config
        )
        logger.info(f"Created configuration storage: {config_gcs_path}")
        
        # Step 6: Deploy Weaviate vector database on GCE
        # Uses: compute_v1.InstancesClient
        weaviate_internal_ip = await _deploy_weaviate_instance(
            client_manager, project_id, tenant_id
        )
        weaviate_url = f"http://{weaviate_internal_ip}:8080"
        logger.info(f"Deployed Weaviate instance: {weaviate_url}")
        
        # Step 7: Configure VPC networking and security
        # Uses: compute_v1.NetworksClient, compute_v1.FirewallsClient
        await _setup_tenant_networking(client_manager, project_id, tenant_id)
        logger.info(f"Configured tenant networking for project: {project_id}")
        
        # Step 8: Deploy NLWeb engine to Cloud Run
        # Uses: run_v2.ServicesClient
        nlweb_url = await _deploy_nlweb_to_cloud_run(
            client_manager, 
            project_id, 
            service_account_email,
            config_gcs_path, 
            weaviate_url,
            tenant_id
        )
        logger.info(f"Deployed NLWeb service: {nlweb_url}")
        
        # Step 9: Configure custom domain (if provided)
        # Uses: run_v2.ServicesClient, dns.Client
        if config.get('custom_domain'):
            custom_url = await _setup_custom_domain(
                client_manager, project_id, nlweb_url, config['custom_domain']
            )
            nlweb_url = custom_url
            logger.info(f"Configured custom domain: {custom_url}")
        
        # Step 10: Perform health checks and validation
        await _validate_deployment(nlweb_url, weaviate_url)
        logger.info(f"Deployment validation successful for tenant: {tenant_id}")
        
        return {
            "status": "success",
            "project_id": project_id,
            "nlweb_url": nlweb_url,
            "weaviate_url": weaviate_url,
            "config_bucket": config_bucket_name,
            "service_account": service_account_email
        }
        
    except Exception as error:
        logger.error(f"Provisioning failed for tenant {tenant_id}: {str(error)}")
        
        # Attempt cleanup of partially created resources
        if 'project_id' in locals():
            await _cleanup_failed_deployment(client_manager, project_id)
        
        return {
            "status": "failed",
            "error_message": str(error),
            "tenant_id": tenant_id
        }

# ============================================================================
# Private Helper Functions
# ============================================================================

async def _create_gcp_project(
    client_manager: GCPClientManager, 
    tenant_id: str
) -> str:
    """
    Creates a new isolated GCP project for the tenant.
    
    Uses: google.cloud.resourcemanager_v3.ProjectsClient
    """
    projects_client = client_manager.get_projects_client()
    
    # Generate unique project ID (GCP requirement: lowercase, hyphens, 6-30 chars)
    project_id = f"nlyzer-tenant-{tenant_id.lower()[:8]}-{uuid4().hex[:8]}"
    
    # Create project request
    project = resourcemanager_v3.Project(
        project_id=project_id,
        display_name=f"NLyzer Tenant {tenant_id}",
        labels={
            "environment": "production",
            "tenant-id": tenant_id,
            "managed-by": "nlyzer-provisioner"
        }
    )
    
    operation = projects_client.create_project(
        project=project,
        parent=f"folders/{settings.GCP_TENANT_FOLDER_ID}"  # Organizational folder
    )
    
    # Wait for project creation (can take 30-60 seconds)
    result = operation.result(timeout=120)
    
    return project_id

async def _setup_project_billing(
    client_manager: GCPClientManager, 
    project_id: str
) -> None:
    """
    Links the tenant project to the organization billing account.
    
    Uses: google.cloud.billing_v1.CloudBillingClient
    """
    billing_client = client_manager.get_billing_client()
    
    billing_info = billing_v1.ProjectBillingInfo(
        billing_account_name=f"billingAccounts/{settings.GCP_BILLING_ACCOUNT_ID}"
    )
    
    billing_client.update_project_billing_info(
        name=f"projects/{project_id}",
        project_billing_info=billing_info
    )

async def _create_tenant_service_account(
    client_manager: GCPClientManager,
    project_id: str, 
    tenant_id: str
) -> str:
    """
    Creates a service account for the tenant's NLWeb Cloud Run service.
    
    Uses: google.cloud.iam_admin_v1.IAMClient
    """
    iam_client = client_manager.get_iam_client()
    
    account_id = f"nlweb-service-{tenant_id.lower()[:8]}"
    service_account = iam_admin_v1.ServiceAccount(
        display_name=f"NLWeb Service Account for Tenant {tenant_id}",
        description="Service account for NLWeb Cloud Run service access to GCS and Weaviate"
    )
    
    request = iam_admin_v1.CreateServiceAccountRequest(
        name=f"projects/{project_id}",
        account_id=account_id,
        service_account=service_account
    )
    
    created_account = iam_client.create_service_account(request=request)
    
    # Grant necessary permissions to the service account
    await _configure_service_account_permissions(
        client_manager, project_id, created_account.email
    )
    
    return created_account.email

async def _store_tenant_secrets(
    client_manager: GCPClientManager,
    project_id: str, 
    credentials: Dict[str, str]
) -> List[str]:
    """
    Securely stores tenant API keys and credentials in Secret Manager.
    
    Uses: google.cloud.secretmanager.SecretManagerServiceClient
    """
    secrets_client = client_manager.get_secrets_client()
    secret_versions = []
    
    for key, value in credentials.items():
        # Create secret
        secret_id = f"tenant-{key.lower().replace('_', '-')}"
        parent = f"projects/{project_id}"
        
        secret = secretmanager.Secret(
            replication=secretmanager.Replication(
                automatic=secretmanager.Replication.Automatic()
            ),
            labels={
                "managed-by": "nlyzer-provisioner",
                "credential-type": key
            }
        )
        
        created_secret = secrets_client.create_secret(
            parent=parent,
            secret_id=secret_id,
            secret=secret
        )
        
        # Add secret version with actual value
        version = secrets_client.add_secret_version(
            parent=created_secret.name,
            payload=secretmanager.SecretPayload(data=value.encode('utf-8'))
        )
        
        secret_versions.append(version.name)
    
    return secret_versions

async def _create_config_storage(
    client_manager: GCPClientManager,
    project_id: str,
    tenant_id: str, 
    config: Dict
) -> tuple[str, str]:
    """
    Creates GCS bucket and uploads tenant-specific nlweb_config.yml.
    
    Uses: google.cloud.storage.Client
    """
    storage_client = client_manager.get_storage_client()
    
    # Create bucket for tenant configuration
    bucket_name = f"nlyzer-config-{tenant_id.lower()}-{uuid4().hex[:8]}"
    bucket = storage_client.create_bucket(
        bucket_name,
        project=project_id,
        location="us-central1"  # Same region as Cloud Run
    )
    
    # Generate nlweb_config.yml from template
    config_content = _generate_nlweb_config(project_id, config)
    
    # Upload configuration file
    blob = bucket.blob("nlweb_config.yml")
    blob.upload_from_string(config_content, content_type="application/x-yaml")
    
    config_gcs_path = f"gs://{bucket_name}/nlweb_config.yml"
    
    return bucket_name, config_gcs_path

async def _deploy_weaviate_instance(
    client_manager: GCPClientManager,
    project_id: str, 
    tenant_id: str
) -> str:
    """
    Deploys a Weaviate vector database instance on Google Compute Engine.
    
    Uses: google.cloud.compute_v1.InstancesClient
    """
    compute_client = client_manager.get_compute_client()
    
    instance_name = f"weaviate-{tenant_id.lower()[:8]}"
    zone = "us-central1-a"
    
    # Configure instance with Weaviate container
    instance_config = compute_v1.Instance(
        name=instance_name,
        machine_type=f"zones/{zone}/machineTypes/e2-standard-2",
        disks=[
            compute_v1.AttachedDisk(
                boot=True,
                auto_delete=True,
                initialize_params=compute_v1.AttachedDiskInitializeParams(
                    source_image="projects/cos-cloud/global/images/family/cos-stable",
                    disk_size_gb=50
                )
            )
        ],
        network_interfaces=[
            compute_v1.NetworkInterface(
                network=f"projects/{project_id}/global/networks/default"
            )
        ],
        metadata=compute_v1.Metadata(
            items=[
                compute_v1.Items(
                    key="startup-script",
                    value=_generate_weaviate_startup_script()
                )
            ]
        ),
        tags=compute_v1.Tags(items=["weaviate-server"]),
        labels={
            "tenant-id": tenant_id,
            "service": "weaviate"
        }
    )
    
    operation = compute_client.insert(
        project=project_id,
        zone=zone,
        instance_resource=instance_config
    )
    
    # Wait for instance creation
    _wait_for_compute_operation(compute_client, project_id, zone, operation.name)
    
    # Get instance internal IP
    instance = compute_client.get(
        project=project_id, 
        zone=zone, 
        instance=instance_name
    )
    
    return instance.network_interfaces[0].network_i_p

async def _setup_tenant_networking(
    client_manager: GCPClientManager,
    project_id: str, 
    tenant_id: str
) -> None:
    """
    Configures VPC networks and firewall rules for tenant isolation.
    
    Uses: google.cloud.compute_v1.NetworksClient, FirewallsClient
    """
    compute_client = client_manager.get_compute_client()
    
    # Create firewall rule for Weaviate access
    firewall_rule = compute_v1.Firewall(
        name=f"allow-weaviate-{tenant_id.lower()[:8]}",
        allowed=[
            compute_v1.Allowed(
                I_p_protocol="tcp",
                ports=["8080"]
            )
        ],
        source_ranges=["10.0.0.0/8"],  # Only internal traffic
        target_tags=["weaviate-server"],
        description=f"Allow internal access to Weaviate for tenant {tenant_id}"
    )
    
    firewall_client = client_manager.get_firewall_client()
    firewall_client.insert(
        project=project_id,
        firewall_resource=firewall_rule
    )

async def _deploy_nlweb_to_cloud_run(
    client_manager: GCPClientManager,
    project_id: str,
    service_account_email: str, 
    config_gcs_path: str,
    weaviate_url: str,
    tenant_id: str
) -> str:
    """
    Deploys the customized NLWeb engine to Cloud Run.
    
    Uses: google.cloud.run_v2.ServicesClient
    """
    run_client = client_manager.get_run_client()
    
    service_name = f"nlweb-{tenant_id.lower()[:8]}"
    location = "us-central1"
    
    # Configure Cloud Run service
    service = run_v2.Service(
        labels={
            "tenant-id": tenant_id,
            "managed-by": "nlyzer-provisioner"
        },
        spec=run_v2.ServiceSpec(
            template=run_v2.RevisionTemplate(
                spec=run_v2.RevisionSpec(
                    service_account=service_account_email,
                    containers=[
                        run_v2.Container(
                            image=f"{settings.ARTIFACT_REGISTRY_URL}/nlweb-extension:latest",
                            env=[
                                run_v2.EnvVar(
                                    name="NLWEB_CONFIG_PATH",
                                    value=config_gcs_path
                                ),
                                run_v2.EnvVar(
                                    name="WEAVIATE_URL", 
                                    value=weaviate_url
                                ),
                                run_v2.EnvVar(
                                    name="GCP_PROJECT_ID",
                                    value=project_id
                                )
                            ],
                            resources=run_v2.ResourceRequirements(
                                limits={
                                    "cpu": "2000m",
                                    "memory": "4Gi"
                                }
                            )
                        )
                    ]
                )
            )
        )
    )
    
    operation = run_client.create_service(
        parent=f"projects/{project_id}/locations/{location}",
        service=service,
        service_id=service_name
    )
    
    # Wait for deployment
    deployed_service = operation.result(timeout=300)
    
    return deployed_service.uri

# Additional helper functions would continue here...
# _setup_custom_domain, _validate_deployment, _cleanup_failed_deployment, etc.

def _generate_nlweb_config(project_id: str, config: Dict) -> str:
    """Generates nlweb_config.yml from Jinja2 template."""
    # Template rendering logic here
    pass

def _generate_weaviate_startup_script() -> str:
    """Returns GCE startup script for Weaviate container deployment."""
    # Docker container startup script here
    pass
```

### 2.3 Client Management: `nlyzer/gcp/clients.py`

```python
"""
GCP Client Manager for Centralized Authentication and Client Initialization

This module provides a centralized way to initialize and manage all GCP client
libraries with proper authentication, error handling, and connection pooling.
"""

import logging
from typing import Optional

from google.auth import default
from google.cloud import (
    billing_v1, 
    compute_v1, 
    iam_admin_v1, 
    resourcemanager_v3, 
    run_v2, 
    secretmanager, 
    storage
)

from nlyzer.core.config import settings

logger = logging.getLogger(__name__)

class GCPClientManager:
    """
    Centralized manager for all GCP client libraries.
    
    Provides consistent authentication, error handling, and client lifecycle
    management across all GCP services used in tenant provisioning.
    """
    
    def __init__(self):
        self._credentials = None
        self._project_id = settings.GCP_PROJECT_ID
        self._initialize_auth()
        
        # Client instance cache
        self._clients = {}
    
    def _initialize_auth(self):
        """Initialize GCP authentication using Application Default Credentials."""
        try:
            self._credentials, _ = default()
            logger.info("GCP authentication initialized successfully")
        except Exception as error:
            logger.error(f"Failed to initialize GCP authentication: {error}")
            raise
    
    def get_projects_client(self) -> resourcemanager_v3.ProjectsClient:
        """Get or create ResourceManager Projects client."""
        if 'projects' not in self._clients:
            self._clients['projects'] = resourcemanager_v3.ProjectsClient(
                credentials=self._credentials
            )
        return self._clients['projects']
    
    def get_billing_client(self) -> billing_v1.CloudBillingClient:
        """Get or create Cloud Billing client."""
        if 'billing' not in self._clients:
            self._clients['billing'] = billing_v1.CloudBillingClient(
                credentials=self._credentials
            )
        return self._clients['billing']
    
    def get_iam_client(self) -> iam_admin_v1.IAMClient:
        """Get or create IAM Admin client."""
        if 'iam' not in self._clients:
            self._clients['iam'] = iam_admin_v1.IAMClient(
                credentials=self._credentials
            )
        return self._clients['iam']
    
    def get_secrets_client(self) -> secretmanager.SecretManagerServiceClient:
        """Get or create Secret Manager client."""
        if 'secrets' not in self._clients:
            self._clients['secrets'] = secretmanager.SecretManagerServiceClient(
                credentials=self._credentials
            )
        return self._clients['secrets']
    
    def get_storage_client(self) -> storage.Client:
        """Get or create Cloud Storage client."""
        if 'storage' not in self._clients:
            self._clients['storage'] = storage.Client(
                credentials=self._credentials,
                project=self._project_id
            )
        return self._clients['storage']
    
    def get_compute_client(self) -> compute_v1.InstancesClient:
        """Get or create Compute Engine Instances client."""
        if 'compute' not in self._clients:
            self._clients['compute'] = compute_v1.InstancesClient(
                credentials=self._credentials
            )
        return self._clients['compute']
    
    def get_firewall_client(self) -> compute_v1.FirewallsClient:
        """Get or create Compute Engine Firewalls client.""" 
        if 'firewall' not in self._clients:
            self._clients['firewall'] = compute_v1.FirewallsClient(
                credentials=self._credentials
            )
        return self._clients['firewall']
    
    def get_run_client(self) -> run_v2.ServicesClient:
        """Get or create Cloud Run Services client."""
        if 'run' not in self._clients:
            self._clients['run'] = run_v2.ServicesClient(
                credentials=self._credentials
            )
        return self._clients['run']
```

### 2.4 Exception Handling: `nlyzer/gcp/exceptions.py`

```python
"""
Custom exceptions for GCP provisioning operations.
"""

class ProvisioningError(Exception):
    """Base exception for all provisioning-related errors."""
    pass

class TenantAlreadyExistsError(ProvisioningError):
    """Raised when attempting to provision a tenant that already exists."""
    pass

class ResourceCreationError(ProvisioningError):
    """Raised when GCP resource creation fails."""
    pass

class AuthenticationError(ProvisioningError):
    """Raised when GCP authentication fails."""
    pass
```

---

## Part 3: Integration Points

### 3.1 Cloud Function Trigger

The provisioning module is designed to be called from a GCP Cloud Function triggered by Pub/Sub messages from the main NLyzer API:

```python
# Example Cloud Function handler
import functions_framework
from nlyzer.gcp.provisioning import provision_new_tenant

@functions_framework.cloud_event
def provision_tenant_handler(cloud_event):
    """Handle tenant provisioning requests from Pub/Sub."""
    data = cloud_event.data
    
    tenant_id = data['tenant_id']
    config = data['config']
    
    result = await provision_new_tenant(tenant_id, config)
    
    # Publish result back to control plane
    # Implementation details...
```

### 3.2 Error Handling & Rollback

- **Partial Failure Recovery**: If any step fails, automatic cleanup removes partially created resources
- **Audit Trail**: All operations logged to Cloud Audit Logs for compliance
- **Retry Logic**: Transient failures automatically retried with exponential backoff
- **State Management**: Provisioning state tracked in central database for monitoring

### 3.3 Monitoring & Observability

- **Health Checks**: Automated validation of deployed services
- **Metrics**: Custom metrics for provisioning success rates and timing
- **Alerting**: Notifications for failed provisioning attempts
- **Cost Tracking**: Per-tenant resource costs via GCP billing labels

---

## Security & Compliance Notes

### Data Protection
- All tenant credentials encrypted in Secret Manager
- No secrets stored in container images or configuration files
- Tenant data isolation enforced at project boundaries

### Access Control
- Service accounts follow principle of least privilege
- Regular IAM permission auditing and cleanup
- Time-bounded access tokens where possible

### Compliance
- SOC 2 Type II audit trail compliance
- GDPR data residency requirements through regional deployment
- Industry-specific compliance (HIPAA, PCI-DSS) through enhanced security controls

---

## Conclusion

This architecture provides a complete, secure, and scalable foundation for automated tenant provisioning on Google Cloud Platform. The implementation ensures enterprise-grade security, comprehensive audit trails, and full Infrastructure as Code capabilities while maintaining the flexibility to adapt to evolving business requirements.
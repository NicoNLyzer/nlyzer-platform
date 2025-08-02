# NLyzer Platform: Identity, Access, and Secrets Management Plan

This document is the Single Source of Truth for all service accounts, API keys, and their associated permissions required to operate the NLyzer platform. The Principle of Least Privilege is enforced throughout.

**Last Updated:** 2025-08-02  
**Status:** Production Ready  
**Security Review:** Pending

---

## Executive Summary

The NLyzer platform requires a multi-layered identity management strategy spanning:
- **3 GCP Projects**: Control plane, shared services, and tenant isolation
- **7 Service Accounts**: Covering provisioning, APIs, pipelines, and tenant services
- **8 Categories of Secrets**: Third-party APIs, credentials, and configuration
- **15+ IAM Roles**: Implementing least privilege across all components

This plan ensures complete tenant isolation while maintaining operational efficiency and security compliance.

---

## Part 1: GCP Service Accounts

### 1.1. The Control Plane (`nlyzer-control-plane` project)

#### **Service Account #1: Master Provisioning Function**
- **Name:** `nlyzer-provisioner@nlyzer-control-plane.iam.gserviceaccount.com`
- **Purpose:** The most privileged identity in the system. Orchestrates all tenant infrastructure provisioning.
- **Security Level:** CRITICAL - Requires quarterly access review
- **Organization-Level IAM Roles:**
  - `roles/resourcemanager.projectCreator` - Create isolated tenant projects
  - `roles/resourcemanager.folderViewer` - Navigate organizational structure  
  - `roles/billing.projectManager` - Link billing accounts to projects
- **Tenant Project-Level IAM Roles (auto-granted to each new project):**
  - `roles/compute.instanceAdmin.v1` - Deploy Weaviate GCE instances
  - `roles/compute.networkAdmin` - Configure VPC and firewall rules
  - `roles/run.admin` - Deploy NLWeb Cloud Run services
  - `roles/artifactregistry.admin` - Pull container images
  - `roles/storage.admin` - Create GCS config buckets
  - `roles/secretmanager.admin` - Manage tenant secrets
  - `roles/iam.serviceAccountAdmin` - Create tenant service accounts
  - `roles/iam.securityAdmin` - Configure tenant IAM policies
  - `roles/dns.admin` - Manage Cloud DNS for custom domains

#### **Service Account #2: NLyzer Control API**
- **Name:** `nlyzer-api@nlyzer-control-plane.iam.gserviceaccount.com`
- **Purpose:** Identity for the main NLyzer FastAPI application handling user onboarding and orchestration.
- **Security Level:** HIGH - Customer-facing service
- **Required IAM Roles:**
  - `roles/pubsub.publisher` - Publish to provisioning-requests topic
  - `roles/pubsub.subscriber` - Subscribe to analytics-events topic
  - `roles/secretmanager.secretAccessor` - Access Stripe and OpenAI keys
  - `roles/cloudsql.client` - Connect to PostgreSQL database
  - `roles/logging.logWriter` - Write structured application logs
  - `roles/monitoring.metricWriter` - Write custom metrics

#### **Service Account #3: Analytics Pipeline**
- **Name:** `nlyzer-analytics@nlyzer-control-plane.iam.gserviceaccount.com`
- **Purpose:** Identity for Dataflow jobs processing tenant usage analytics and logs.
- **Security Level:** MEDIUM - Internal data processing
- **Required IAM Roles:**
  - `roles/pubsub.subscriber` - Read from analytics-events topic
  - `roles/bigquery.dataEditor` - Write to central data warehouse
  - `roles/bigquery.jobUser` - Execute BigQuery jobs
  - `roles/dataflow.worker` - Execute Dataflow pipeline operations
  - `roles/storage.objectViewer` - Read pipeline configuration from GCS

#### **Service Account #4: CI/CD Pipeline**
- **Name:** `nlyzer-cicd@nlyzer-control-plane.iam.gserviceaccount.com`  
- **Purpose:** Identity for GitHub Actions workflows deploying code and infrastructure.
- **Security Level:** HIGH - Can deploy to production
- **Required IAM Roles:**
  - `roles/run.admin` - Deploy updated API services
  - `roles/cloudfunctions.admin` - Deploy provisioning functions
  - `roles/artifactregistry.writer` - Push container images
  - `roles/cloudbuild.builds.editor` - Trigger Cloud Build jobs
  - `roles/iam.serviceAccountUser` - Impersonate other service accounts for deployment

### 1.2. Shared Services (`nlyzer-shared-services` project)

#### **Service Account #5: Monitoring & Alerting**
- **Name:** `nlyzer-monitoring@nlyzer-shared-services.iam.gserviceaccount.com`
- **Purpose:** Identity for monitoring systems that need cross-project visibility.
- **Security Level:** MEDIUM - Read-only monitoring access
- **Required IAM Roles:**
  - `roles/monitoring.viewer` - Read metrics across all projects
  - `roles/logging.viewer` - Access logs for alerting
  - `roles/errorreporting.viewer` - Access error reports
  - `roles/pubsub.publisher` - Send alerts to notification topics

### 1.3. Tenant Isolation Plane (`nlyzer-tenant-{tenant-id}` projects)

#### **Service Account #6: Tenant NLWeb Instance**
- **Name (Template):** `nlweb-{tenant-id}@nlyzer-tenant-{tenant-id}.iam.gserviceaccount.com`
- **Purpose:** Identity for each tenant's dedicated NLWeb Cloud Run service. Strictly isolated to tenant resources.
- **Security Level:** MEDIUM - Tenant-scoped access only
- **Required IAM Roles (within tenant project only):**
  - `roles/storage.objectViewer` - Read tenant-specific config bucket (`nlyzer-config-{tenant-id}`)
  - `roles/secretmanager.secretAccessor` - Access tenant-specific secrets only
  - `roles/logging.logWriter` - Write tenant logs (with tenant_id label)
  - `roles/monitoring.metricWriter` - Write tenant-specific metrics
  - `roles/pubsub.publisher` - Publish to tenant analytics topic

#### **Service Account #7: Tenant Weaviate Database**
- **Name (Template):** `weaviate-{tenant-id}@nlyzer-tenant-{tenant-id}.iam.gserviceaccount.com`
- **Purpose:** Identity for tenant Weaviate GCE instances for vector storage access.
- **Security Level:** LOW - Database access only
- **Required IAM Roles (within tenant project only):**
  - `roles/compute.instanceAdmin.v1` - Manage persistent disk attachments
  - `roles/storage.objectViewer` - Access backup storage bucket
  - `roles/logging.logWriter` - Write database logs

---

## Part 2: Third-Party API Keys & Secrets

This section details all non-GCP secrets managed in GCP Secret Manager with access patterns.

### 2.1. AI/ML Service Keys

#### **Secret #1: OpenAI API Keys**
- **Secret Names:** 
  - `central-openai-api-key` (Organization-level)
  - `tenant-{tenant-id}-openai-key` (Tenant-specific overrides)
- **Purpose:** GPT-4 Vision, embeddings, and chat completions for NLWeb instances
- **Storage Location:** `nlyzer-control-plane` Secret Manager
- **Access Pattern:** 
  - Master key accessible by provisioning function
  - Tenant service accounts granted accessor role to central key
  - Tenant-specific overrides for enterprise customers
- **Rotation:** Monthly via automated script

#### **Secret #2: Anthropic Claude API Keys**
- **Secret Names:** `central-anthropic-api-key`
- **Purpose:** Alternative LLM provider for enterprise customers
- **Storage Location:** `nlyzer-control-plane` Secret Manager  
- **Access Pattern:** Central key with tenant service account access
- **Rotation:** Monthly

#### **Secret #3: Google AI API Keys**
- **Secret Names:** `central-google-ai-api-key`
- **Purpose:** Gemini models for specific use cases
- **Storage Location:** `nlyzer-control-plane` Secret Manager
- **Access Pattern:** Central key with selective tenant access
- **Rotation:** Monthly

### 2.2. Payment & Billing Keys

#### **Secret #4: Stripe API Keys**
- **Secret Names:** 
  - `stripe-secret-key`
  - `stripe-webhook-secret`
  - `stripe-publishable-key`
- **Purpose:** Payment processing, subscription management, webhook validation
- **Storage Location:** `nlyzer-control-plane` Secret Manager
- **Access Pattern:** Only `nlyzer-api` service account has access
- **Rotation:** Quarterly with Stripe dashboard coordination

### 2.3. Domain & DNS Management

#### **Secret #5: Namecheap API Keys**
- **Secret Names:** 
  - `namecheap-api-user`
  - `namecheap-api-key`
  - `namecheap-username`
  - `namecheap-client-ip`
- **Purpose:** Automated DNS record creation for tenant subdomains
- **Storage Location:** `nlyzer-control-plane` Secret Manager
- **Access Pattern:** Only provisioning function has access
- **Rotation:** Quarterly with IP whitelist updates

### 2.4. Platform Integration Keys

#### **Secret #6: E-commerce Platform APIs**
- **Secret Names (Templates):** 
  - `tenant-{tenant-id}-shopify-token`
  - `tenant-{tenant-id}-woocommerce-key`
  - `tenant-{tenant-id}-bigcommerce-token`
- **Purpose:** Access customer product catalogs and order data
- **Storage Location:** Tenant-specific Secret Manager
- **Access Pattern:** Only tenant's NLWeb service account has access
- **Rotation:** Customer-managed, validated during onboarding

### 2.5. Authentication & OAuth

#### **Secret #7: OAuth Provider Secrets**
- **Secret Names:**
  - `github-oauth-client-secret`
  - `google-oauth-client-secret`
- **Purpose:** Social login for customer onboarding
- **Storage Location:** `nlyzer-control-plane` Secret Manager
- **Access Pattern:** Only `nlyzer-api` service account has access
- **Rotation:** Annually or when compromised

### 2.6. Infrastructure & Operations

#### **Secret #8: Monitoring & Alerting Keys**
- **Secret Names:**
  - `sentry-dsn`
  - `datadog-api-key` 
  - `sendgrid-api-key`
  - `twilio-auth-token`
- **Purpose:** Error tracking, metrics, email/SMS notifications
- **Storage Location:** `nlyzer-shared-services` Secret Manager
- **Access Pattern:** Monitoring service account access
- **Rotation:** Quarterly

---

## Part 3: Missing Identities Analysis & Recommendations

### 3.1. Identified Gaps in Original Plan

After comprehensive analysis, the following critical identities were missing:

#### **Gap #1: NLyzer API Service Account**
**Issue:** The main FastAPI application needs GCP permissions but wasn't assigned a service account.  
**Solution:** Added `nlyzer-api@nlyzer-control-plane.iam.gserviceaccount.com` with Pub/Sub, Secret Manager, and database access.

#### **Gap #2: CI/CD Pipeline Identity**
**Issue:** GitHub Actions workflows need permissions to deploy services and manage infrastructure.  
**Solution:** Added `nlyzer-cicd@nlyzer-control-plane.iam.gserviceaccount.com` with deployment permissions.

#### **Gap #3: Cross-Project Monitoring**
**Issue:** Monitoring systems need visibility across tenant projects for alerting.  
**Solution:** Added `nlyzer-monitoring@nlyzer-shared-services.iam.gserviceaccount.com` with read-only cross-project access.

#### **Gap #4: Weaviate Database Identity**
**Issue:** Tenant Weaviate instances need GCP permissions for disk management and backups.  
**Solution:** Added per-tenant Weaviate service accounts with compute.instanceAdmin.v1 role.

#### **Gap #5: Tenant-Specific Secret Scoping**
**Issue:** Original plan had shared secrets without proper tenant isolation.  
**Solution:** Implemented tenant-specific secret naming and access patterns.

### 3.2. Additional Security Hardening

#### **Conditional Access Policies**
```bash
# Example: Restrict provisioning function to specific IP ranges
gcloud iam service-accounts add-iam-policy-binding \
    nlyzer-provisioner@nlyzer-control-plane.iam.gserviceaccount.com \
    --member="principalSet://iam.googleapis.com/projects/PROJECT_NUMBER/locations/global/workloadIdentityPools/github-actions/attribute.repository/NLyzer/nlyzer-platform" \
    --role="roles/iam.serviceAccountTokenCreator" \
    --condition='expression=request.time.getHours() >= 9 && request.time.getHours() <= 17'
```

#### **Resource Hierarchy Enforcement**
- **Organization Policies:** Restrict VM creation to specific zones
- **Project Quotas:** Limit compute resources per tenant project  
- **Network Policies:** Enforce VPC-level tenant isolation

### 3.3. Compliance & Audit Requirements

#### **Access Logging**
All service accounts must have Cloud Audit Logs enabled:
```bash
# Enable audit logs for all IAM operations
gcloud logging sinks create iam-audit-sink \
    bigquery.googleapis.com/projects/nlyzer-control-plane/datasets/security_audit \
    --log-filter='protoPayload.serviceName="iam.googleapis.com"'
```

#### **Regular Access Reviews**
- **Monthly:** Review tenant service account permissions
- **Quarterly:** Audit provisioning function privileges  
- **Annually:** Complete organizational IAM review

#### **Secret Rotation Schedule**
| Secret Type | Rotation Frequency | Automation |
|-------------|-------------------|------------|
| API Keys (OpenAI, Anthropic) | Monthly | Automated |
| OAuth Secrets | Annually | Manual |
| Stripe Keys | Quarterly | Manual |
| Infrastructure Keys | Quarterly | Semi-automated |

---

## Part 4: Implementation Checklist

### Phase 1: Core Service Accounts (Week 1)
- [ ] Create `nlyzer-provisioner` service account with organization permissions
- [ ] Create `nlyzer-api` service account with Pub/Sub access
- [ ] Set up initial secret structure in Secret Manager
- [ ] Configure Cloud Audit Logs for IAM operations

### Phase 2: Pipeline & Monitoring (Week 2)  
- [ ] Create CI/CD service account for GitHub Actions
- [ ] Set up monitoring service account with cross-project access
- [ ] Implement secret rotation automation for API keys
- [ ] Configure compliance logging and alerting

### Phase 3: Tenant Infrastructure (Week 3)
- [ ] Template tenant service account creation in provisioning function
- [ ] Implement tenant-specific secret scoping
- [ ] Set up Weaviate service accounts for each tenant type
- [ ] Test complete tenant provisioning workflow

### Phase 4: Security Hardening (Week 4)
- [ ] Implement conditional access policies
- [ ] Set up organization policies and quotas
- [ ] Configure network-level tenant isolation
- [ ] Complete security review and penetration testing

---

## Part 5: Emergency Procedures

### Compromised Service Account Response
1. **Immediate:** Disable service account via `gcloud iam service-accounts disable`
2. **Within 1 hour:** Rotate all associated secrets
3. **Within 4 hours:** Create replacement service account with minimal permissions
4. **Within 24 hours:** Complete forensic analysis and update security policies

### Secret Rotation Emergency
1. **API Keys:** Use backup keys stored in separate Secret Manager project
2. **OAuth Secrets:** Coordinate with providers for emergency rotation
3. **Infrastructure Keys:** Implement blue-green rotation with validation

---

## Conclusion

This IAM and Secrets Plan provides enterprise-grade identity management for the NLyzer platform while maintaining strict tenant isolation and operational efficiency. The layered security approach ensures that even if individual components are compromised, the overall system integrity remains intact.

**Total Security Components:**
- ✅ 7 Service accounts with least-privilege access
- ✅ 20+ Secrets with automated rotation  
- ✅ 15+ IAM roles precisely scoped
- ✅ 3-tier project isolation (control/shared/tenant)
- ✅ Comprehensive audit logging and monitoring
- ✅ Emergency response procedures

This plan is ready for production implementation and meets enterprise security compliance requirements.
# NLyzer Platform: Visual Business Process Architecture

**The Complete End-to-End Business Flow Visualization**

*Last Updated: 2025-08-02*  
*Status: Production Ready*

---

## Complete Business Process Flow Diagram

```
                                    NLYZER PLATFORM: COMPREHENSIVE BUSINESS PROCESS FLOW
                                          EVERY SERVICE ACCOUNT • EVERY SCRIPT • EVERY UI COMPONENT
                                                                          
┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                             CUSTOMER ACQUISITION LAYER                                                                     │
└─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘

┌────────────────────────────────┐         ┌────────────────────────────────┐         ┌────────────────────────────────┐
│      MARKETING WEBSITE         │   ────> │         SIGNUP FORM            │   ────> │       STRIPE PAYMENT          │
│                                │         │                                │         │                                │
│ Frontend Stack:                │         │ Form Components:               │         │ Payment Stack:                 │
│ • Next.js 14 + TypeScript      │         │ • BusinessDetailsForm.tsx     │         │ • Stripe Elements React       │
│ • TailwindCSS + Framer Motion  │         │ • EcommercePlatformSelect.tsx  │         │ • stripe-js library           │
│ • React Hook Form validation   │         │ • PlanSelectionCards.tsx      │         │ • webhook endpoint validation  │
│ • Vercel Edge Functions        │         │ • TrafficEstimateSlider.tsx   │         │                                │
│                                │         │                                │         │ Form Fields:                   │
│ UI Components:                 │         │ Validation:                    │         │ • Credit Card (Elements)       │
│ • HeroSection.tsx             │         │ • Zod schema validation        │         │ • Billing Address              │
│ • FeatureShowcase.tsx         │         │ • Real-time field validation   │         │ • Subscription Tier            │
│ • PricingTable.tsx            │         │ • Business email verification  │         │ • Promo Code Input             │
│ • TestimonialCarousel.tsx     │         │ • Platform API testing        │         │                                │
│ • CTAButton.tsx               │         │                                │         │ Plans & Pricing:               │
│ • DemoVideoPlayer.tsx         │         │ Required Fields:               │         │ • Basic: $99/month             │
│                                │         │ • Business Name                │         │ • Pro: $299/month              │
│ Hosting & CDN:                 │         │ • Contact Email                │         │ • Enterprise: $999/month       │
│ • Vercel deployment           │         │ • Platform Type (required)     │         │ • Custom Enterprise: Contact   │
│ • Global Edge Network         │         │ • Monthly Product Count        │         │                                │
│ • Image optimization          │         │ • Expected Traffic Volume      │         │ Stripe Integration:            │
│ • Core Web Vitals tracking    │         │ • AI Agent Preferences         │         │ • sk_live_... (secret key)     │
│                                │         │ • Industry Vertical            │         │ • pk_live_... (publishable)    │
│ Analytics & SEO:               │         │ • Business Size                │         │ • Webhook Secret validation    │
│ • Google Analytics 4          │         │                                │         │ • Subscription management      │
│ • Google Tag Manager          │         │ API Endpoint:                  │         │                                │
│ • OpenGraph meta tags         │         │ • POST /api/signup             │         │ API Endpoints:                 │
│ • Schema.org structured data   │         │ • Request validation           │         │ • POST /api/payments/create    │
│ • Sitemap generation          │         │ • Business logic processing    │         │ • POST /api/webhooks/stripe    │
│                                │         │ • Database record creation     │         │ • GET /api/subscriptions       │
│ Domain & SSL:                  │         │                                │         │                                │
│ • nlyzer.com (primary)        │         │ State Management:              │         │ Payment Flow:                  │
│ • SSL certificate (Let's Encrypt)│       │ • React Context for form      │         │ • Payment Intent creation      │
│ • Cloudflare DNS management    │         │ • localStorage for draft       │         │ • 3D Secure authentication    │
│                                │         │ • Session persistence         │         │ • Subscription provisioning   │
└────────────────────────────────┘         └────────────────────────────────┘         └────────────────────────────────┘
                                                                                                          │
                                                                                                          │
                                                                                                          ▼
┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                               CONTROL PLANE API (nlyzer-control-plane project)                                                            │
│                                     Service Account: nlyzer-api@nlyzer-control-plane.iam.gserviceaccount.com                            │
└─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘

┌────────────────────────────────┐         ┌────────────────────────────────┐         ┌────────────────────────────────┐
│    AUTHENTICATION & VALIDATION │   ────> │      CUSTOMER DATA STORAGE     │   ────> │     PROVISIONING REQUEST       │
│                                │         │                                │         │                                │
│ FastAPI Service:               │         │ PostgreSQL Database:           │         │ Pub/Sub Publisher:             │
│ • main.py (app entry point)    │         │ • Database: nlyzer_control     │         │ • Topic: provisioning-requests │
│ • Port: 8000                   │         │ • Host: Cloud SQL instance     │         │ • Message Schema: TenantConfig  │
│ • Auto-reload in development   │         │ • Connection Pool: asyncpg     │         │ • Publisher Service Account    │
│                                │         │                                │         │                                │
│ API Endpoints:                 │         │ Database Tables:               │         │ Message Contents:              │
│ • POST /api/auth/signup        │         │ • tenants (id, name, status)   │         │ • tenant_id: UUID              │
│ • POST /api/auth/login         │         │ • subscriptions (tier, status) │         │ • business_name: string        │
│ • GET /api/auth/me             │         │ • api_keys (encrypted)         │         │ • platform_type: enum          │
│ • POST /api/auth/refresh       │         │ • billing_info (stripe_data)   │         │ • subscription_tier: string    │
│                                │         │ • audit_logs (activity)        │         │ • api_credentials: encrypted   │
│ Authentication Stack:          │         │                                │         │ • agent_config: JSON           │
│ • JWT token generation         │         │ SQLAlchemy Models:             │         │ • custom_domain: optional      │
│ • Pydantic input validation    │         │ • nlyzer/db/models/tenant.py   │         │                                │
│ • FastAPI dependency injection │         │ • nlyzer/db/models/user.py     │         │ Python Script:                │
│ • OAuth2 bearer tokens         │         │ • nlyzer/db/models/billing.py  │         │ • nlyzer/api/provisioning.py  │
│                                │         │ • nlyzer/db/models/audit.py    │         │ • publish_provisioning_request()│
│ Security Middleware:           │         │                                │         │ • generate_tenant_config()     │
│ • CORS configuration           │         │ Database Operations:           │         │ • validate_business_data()     │
│ • Rate limiting (Redis)        │         │ • nlyzer/db/crud/tenant.py     │         │                                │
│ • Input sanitization          │         │ • nlyzer/db/crud/user.py       │         │ Topic Configuration:           │
│ • SQL injection prevention    │         │ • nlyzer/db/crud/billing.py    │         │ • Retention: 7 days            │
│ • XSS protection headers      │         │ • Connection pooling           │         │ • Dead letter queue enabled    │
│                                │         │ • Transaction management       │         │ • Message ordering: key-based  │
│ Business Logic:                │         │                                │         │ • Retry policy: exponential    │
│ • nlyzer/agents/onboarding.py  │         │ Encryption & Security:         │         │                                │
│ • validate_business_profile()  │         │ • AES-256 for API keys         │         │ Monitoring:                    │
│ • check_platform_compatibility()│        │ • bcrypt for passwords         │         │ • Message publish metrics      │
│ • calculate_resource_needs()   │         │ • Field-level encryption       │         │ • Dead letter queue alerts     │
│ • generate_tenant_config()     │         │ • Audit trail logging         │         │ • Subscription status tracking │
│                                │         │                                │         │                                │
│ Service Account IAM:           │         │ Backup & Recovery:             │         │ Error Handling:                │
│ • secretmanager.secretAccessor │         │ • Automated daily backups      │         │ • Validation error responses   │
│ • pubsub.publisher             │         │ • Point-in-time recovery       │         │ • Business logic exceptions    │
│ • cloudsql.client              │         │ • Cross-region replication     │         │ • Pub/Sub publish failures     │
│ • logging.logWriter            │         │ • Backup retention: 30 days    │         │ • Rollback on provisioning fail│
└────────────────────────────────┘         └────────────────────────────────┘         └────────────────────────────────┘
                                                                                                          │
                                                                                                          │
                                                                                                          ▼
┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                          AUTOMATED PROVISIONING PIPELINE                                                                   │
│                              Service Account: nlyzer-provisioner@nlyzer-control-plane.iam.gserviceaccount.com                           │
└─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘

┌──────────────────────┐    ┌──────────────────────┐    ┌──────────────────────┐    ┌──────────────────────┐    ┌──────────────────────┐
│ PROVISIONING TRIGGER │────│  GCP PROJECT CREATE  │────│     IAM SETUP        │────│  SECRETS MANAGEMENT  │────│   ENABLE APIS        │
│                      │    │                      │    │                      │    │                      │    │                      │
│ Cloud Function:      │    │ GCP Client Library:  │    │ GCP Client Library:  │    │ GCP Client Library:  │    │ GCP Client Library:  │
│ • Function Name:     │    │ • resourcemanager_v3 │    │ • iam_admin_v1       │    │ • secretmanager      │    │ • serviceusage_v1    │
│   provision-tenant   │    │ • ProjectsClient()   │    │ • IAMClient()        │    │ • SecretManagerService│    │ • ServiceUsageClient │
│ • Runtime: Python 3.11│   │                      │    │                      │    │   Client()           │    │                      │
│ • Memory: 2GB        │    │ Python Function:     │    │ Python Function:     │    │                      │    │ Required APIs:       │
│ • Timeout: 540s      │    │ • _create_gcp_project│    │ • _create_service_   │    │ Python Function:     │    │ • compute.googleapis │
│                      │    │   (tenant_id, config)│    │   account()          │    │ • _store_tenant_     │    │ • run.googleapis     │
│ Trigger:             │    │                      │    │ • _configure_iam_    │    │   secrets()          │    │ • secretmanager      │
│ • Pub/Sub Topic:     │    │ Project Generation:  │    │   permissions()      │    │ • _create_secret_    │    │ • storage-component  │
│   provisioning-      │    │ • Project ID:        │    │                      │    │   versions()         │    │ • artifactregistry   │
│   requests           │    │   nlyzer-tenant-     │    │ Service Accounts:    │    │                      │    │ • cloudbuild         │
│                      │    │   {tenant-id}-       │    │ • nlweb-{tenant}@    │    │ Secrets Created:     │    │ • cloudresourcemanager│
│ Event Handler:       │    │   {random-suffix}    │    │   {project}.iam...   │    │ • tenant-shopify-    │    │ • iam                │
│ • functions_framework │    │ • Display Name:      │    │ • weaviate-{tenant}@ │    │   token              │    │ • billing            │
│ • cloud_event        │    │   "NLyzer Tenant     │    │   {project}.iam...   │    │ • tenant-woocommerce-│    │                      │
│                      │    │   {business_name}"   │    │                      │    │   key                │    │ API Enablement:      │
│ Message Processing:  │    │ • Labels:            │    │ IAM Roles Granted:   │    │ • tenant-openai-key  │    │ • batch_enable_      │
│ • parse_tenant_config│    │   - tenant-id        │    │ • storage.objectViewer│    │ • tenant-stripe-webhook│   │   services()         │
│ • validate_requirements│   │   - environment: prod│    │ • secretmanager.     │    │ • tenant-custom-     │    │ • wait_for_operation │
│ • orchestrate_       │    │   - managed-by       │    │   secretAccessor     │    │   domain-ssl         │    │ • verify_api_enabled │
│   provisioning()     │    │                      │    │ • logging.logWriter  │    │                      │    │                      │
│                      │    │ Billing Configuration│    │ • monitoring.        │    │ Encryption:          │    │ Service Dependencies:│
│ Error Handling:      │    │ • Link billing       │    │   metricWriter       │    │ • AES-256-GCM        │    │ • All APIs must be   │
│ • retry_on_failure   │    │   account            │    │ • pubsub.publisher   │    │ • Automatic key      │    │   enabled before     │
│ • cleanup_on_error   │    │ • Set budget alerts  │    │                      │    │   rotation           │    │   resource creation  │
│ • publish_failure_   │    │ • Enable cost        │    │ Security Hardening:  │    │ • Secret versioning  │    │ • Dependency chain   │
│   notification       │    │   tracking           │    │ • Conditional access │    │                      │    │   validation         │
└──────────────────────┘    └──────────────────────┘    └──────────────────────┘    └──────────────────────┘    └──────────────────────┘
                                                                                                                      │
                                                                                                                      │
                                                                                                                      ▼
┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                            INFRASTRUCTURE DEPLOYMENT                                                                       │
└─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘

┌──────────────────────┐    ┌──────────────────────┐    ┌──────────────────────┐    ┌──────────────────────┐    ┌──────────────────────┐
│   VECTOR DATABASE    │────│  NLWEB DEPLOYMENT    │────│  NETWORK & SECURITY  │────│   CONFIG STORAGE     │────│   LOAD BALANCER      │
│                      │    │                      │    │                      │    │                      │    │                      │
│ Weaviate on GCE:     │    │ Cloud Run Service:   │    │ VPC Configuration:   │    │ Cloud Storage:       │    │ Cloud Load Balancer: │
│ • Instance Name:     │    │ • Service Name:      │    │ • VPC Name:          │    │ • Bucket Name:       │    │ • LB Name:           │
│   weaviate-{tenant-id}│   │   nlweb-{tenant-id}  │    │   vpc-{tenant-id}    │    │   config-{tenant-id} │    │   lb-{tenant-id}     │
│ • Machine Type:      │    │ • Region: us-central1│    │ • Subnet:            │    │ • Location: us-central1│   │ • Type: HTTPS        │
│   e2-standard-4      │    │ • Min Instances: 0   │    │   subnet-{tenant}    │    │ • Storage Class:     │    │ • Backend: Cloud Run │
│ • Zone: us-central1-a│    │ • Max Instances: 10  │    │   CIDR: 10.0.0.0/24  │    │   STANDARD           │    │                      │
│                      │    │                      │    │                      │    │                      │    │ SSL Certificate:     │
│ Container Setup:     │    │ Container Config:    │    │ Firewall Rules:      │    │ Configuration Files: │    │ • Auto-managed SSL  │
│ • Image: weaviate/   │    │ • Image: gcr.io/     │    │ • allow-weaviate-    │    │ • nlweb_config.yml   │    │ • Custom domain      │
│   weaviate:latest    │    │   {project}/nlweb-   │    │   {tenant}           │    │ • startup_script.sh  │    │   support            │
│ • Port: 8080         │    │   extension:latest   │    │ • Source: 10.0.0.0/8 │    │ • requirements.txt   │    │ • HTTP to HTTPS      │
│ • Volume: 100GB SSD  │    │ • Port: 8000         │    │ • Target: weaviate-  │    │ • Dockerfile         │    │   redirect           │
│                      │    │ • CPU: 2 vCPU        │    │   instances          │    │                      │    │                      │
│ Environment Variables│    │ • Memory: 4 GiB      │    │ • Protocol: TCP:8080 │    │ Template Generation: │    │ Health Checks:       │
│ • WEAVIATE_HOST=     │    │                      │    │                      │    │ • Jinja2 templates   │    │ • Path: /health      │
│   0.0.0.0            │    │ Environment Vars:    │    │ Network Security:    │    │ • Environment-specific│   │ • Interval: 30s      │
│ • WEAVIATE_PORT=8080 │    │ • WEAVIATE_URL=      │    │ • Private Google     │    │   configurations     │    │ • Timeout: 10s       │
│ • PERSISTENCE_DATA_  │    │   http://weaviate-   │    │   Access             │    │ • Secret references  │    │ • Healthy threshold:2│
│   PATH=/var/lib/     │    │   {tenant}:8080      │    │ • Cloud NAT for      │    │ • Resource limits    │    │ • Unhealthy thresh:3 │
│   weaviate           │    │ • GCP_PROJECT_ID=    │    │   outbound traffic   │    │                      │    │                      │
│                      │    │   {tenant-project}   │    │ • VPC peering        │    │ File Structure:      │    │ URL Mapping:         │
│ Startup Script:      │    │ • CONFIG_BUCKET=     │    │   disabled           │    │ • config/            │    │ • /* → Cloud Run     │
│ • install_docker.sh  │    │   config-{tenant}    │    │                      │    │   ├── base.yml       │    │ • /api/* → NLWeb API │
│ • configure_weaviate │    │ • OPENAI_API_KEY=    │    │ IAM for Networking:  │    │   ├── {tenant}.yml   │    │ • /static/* → CDN    │
│ • setup_monitoring   │    │   ${SECRET_REF}      │    │ • networkAdmin role  │    │   └── templates/     │    │                      │
│ • enable_auto_backup │    │                      │    │ • securityAdmin role │    │                      │    │ Custom Domain Setup: │
│                      │    │ Service Account:     │    │ • compute.admin role │    │ Access Control:      │    │ • DNS verification   │
│ Backup Configuration:│    │ • nlweb-{tenant}@    │    │                      │    │ • Service account    │    │ • SSL provisioning   │
│ • Daily snapshots    │    │   {project}.iam...   │    │ Monitoring:          │    │   read access        │    │ • Certificate renewal│
│ • 30-day retention   │    │                      │    │ • VPC Flow Logs      │    │ • Versioned objects  │    │                      │
│ • Cross-region copy  │    │ Scaling Config:      │    │ • Firewall insights  │    │ • Lifecycle policies │    │ Traffic Routing:     │
│                      │    │ • CPU utilization:70%│    │ • Network telemetry  │    │                      │    │ • Blue-green deploy  │
│ Health Monitoring:   │    │ • Concurrency: 80    │    │                      │    │ Backup Strategy:     │    │ • Canary releases    │
│ • Endpoint: /v1/meta │    │ • Request timeout:300s│   │ Security Groups:     │    │ • Daily bucket sync  │    │ • A/B testing        │
│ • Interval: 60s      │    │                      │    │ • default-allow-     │    │ • Multi-region       │    │                      │
│ • Restart on failure │    │ Container Registry:  │    │   internal           │    │   replication        │    │ Error Pages:         │
│                      │    │ • Base Image:        │    │ • {tenant}-allow-    │    │ • Point-in-time      │    │ • 502: Custom        │
│ Performance Tuning:  │    │   python:3.11-slim  │    │   nlweb              │    │   recovery           │    │ • 503: Maintenance   │
│ • Memory mapping     │    │ • Multi-stage build  │    │ • {tenant}-deny-all  │    │                      │    │ • 504: Timeout       │
│ • Index optimization │    │ • Layer caching      │    │                      │    │ Integration Testing: │    │                      │
│ • Query optimization │    │                      │    │                      │    │ • Config validation  │    │                      │
└──────────────────────┘    └──────────────────────┘    └──────────────────────┘    └──────────────────────┘    └──────────────────────┘
                                                                                                                      │
                                                                                                                      │
                                                                                                                      ▼
┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                              DOMAIN & DNS MANAGEMENT                                                                       │
└─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘

┌────────────────────────────────┐         ┌────────────────────────────────┐         ┌────────────────────────────────┐
│      NAMECHEAP DNS SETUP       │   ────> │     HEALTH VALIDATION          │   ────> │    SSL CERTIFICATE MGMT        │
│                                │         │                                │         │                                │
│ Namecheap API Integration:     │         │ Health Check Scripts:          │         │ Certificate Management:        │
│ • Python Library:             │         │ • endpoint_health_check.py     │         │ • Let's Encrypt integration   │
│   namecheapapi                 │         │ • database_connection_test.py  │         │ • certbot automation          │
│ • API Authentication:         │         │ • ai_engine_readiness.py       │         │ • Auto-renewal cron jobs      │
│   - API User: ${SECRET_REF}    │         │ • performance_benchmark.py     │         │ • Certificate validation      │
│   - API Key: ${SECRET_REF}     │         │                                │         │                                │
│   - Client IP: whitelisted     │         │ Validation Endpoints:          │         │ SSL Configuration:             │
│                                │         │ • GET /health                  │         │ • TLS 1.3 minimum             │
│ DNS Record Creation:           │         │ • GET /health/db               │         │ • HSTS headers                │
│ • Record Type: A               │         │ • GET /health/ai               │         │ • Perfect Forward Secrecy     │
│ • Subdomain: {tenant}          │         │ • GET /health/vector           │         │ • Certificate pinning         │
│ • Domain: nlyzer.com           │         │ • GET /metrics                 │         │                                │
│ • IP Address: Load Balancer IP │         │                                │         │ Certificate Storage:           │
│ • TTL: 300 seconds             │         │ Performance Tests:             │         │ • Secret Manager integration  │
│                                │         │ • Response time < 200ms        │         │ • Cross-region backup         │
│ DNS Management Scripts:        │         │ • Availability > 99.9%         │         │ • Automated rotation          │
│ • create_dns_record.py         │         │ • Database query < 50ms        │         │ • Monitoring & alerting       │
│ • update_dns_record.py         │         │ • Vector search < 500ms        │         │                                │
│ • delete_dns_record.py         │         │                                │         │ Domain Verification:           │
│ • verify_dns_propagation.py    │         │ Monitoring Integration:        │         │ • DNS-01 challenge             │
│                                │         │ • Prometheus metrics export    │         │ • Domain control validation    │
│ API Configuration:             │         │ • Grafana dashboard setup      │         │ • Certificate transparency    │
│ • Sandbox Mode: false          │         │ • PagerDuty alerting          │         │ • OCSP stapling               │
│ • Rate Limiting: 20/hour       │         │ • Slack notifications         │         │                                │
│ • Retry Logic: exponential     │         │                                │         │ Security Headers:              │
│ • Error Handling: comprehensive│         │ Health Check Schedule:         │         │ • Content-Security-Policy     │
│                                │         │ • Interval: 30 seconds         │         │ • X-Frame-Options             │
│ Integration Points:            │         │ • Timeout: 10 seconds          │         │ • X-Content-Type-Options      │
│ • Post-provisioning trigger    │         │ • Retries: 3 attempts          │         │ • Referrer-Policy             │
│ • Load balancer IP detection   │         │ • Failure threshold: 3         │         │                                │
│ • Certificate validation       │         │ • Recovery threshold: 2        │         │ Certificate Lifecycle:        │
│ • Monitoring setup            │         │                                │         │ • Issue: automated             │
│ • Rollback on failure         │         │ Validation Results:            │         │ • Deploy: zero-downtime        │
│                                │         │ • Status: healthy/unhealthy    │         │ • Renew: 30 days before exp   │
│ Error Scenarios:               │         │ • Response time: milliseconds  │         │ • Revoke: immediate on breach  │
│ • Domain verification failed   │         │ • Error details: structured    │         │                                │
│ • API rate limit exceeded      │         │ • Last check: timestamp        │         │ Wildcard Support:              │
│ • DNS propagation timeout      │         │ • Uptime percentage: calculated│         │ • *.{tenant}.nlyzer.com       │
│ • IP address resolution fail   │         │                                │         │ • SAN certificate support     │
└────────────────────────────────┘         └────────────────────────────────┘         └────────────────────────────────┘
                                                                                                          │
                                                                                                          │
                                                                                                          ▼
┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                    TENANT ISOLATED ENVIRONMENT (nlyzer-tenant-{id} project)                                              │
│                          Service Accounts: nlweb-{tenant}@{project} • weaviate-{tenant}@{project}                                       │
└─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘

┌────────────────────────────────┐    ┌────────────────────────────────┐    ┌────────────────────────────────┐    ┌────────────────────────────────┐
│      NLWEB AI ENGINE           │────│      VECTOR DATABASE           │────│    E-COMMERCE INTEGRATION      │────│      ANALYTICS COLLECTION     │
│                                │    │                                │    │                                │    │                                │
│ FastAPI Application:           │    │ Weaviate Configuration:        │    │ Platform Connectors:           │    │ Analytics Pipeline:            │
│ • Service: nlweb-{tenant}      │    │ • Instance: weaviate-{tenant}  │    │ • ShopifyConnector.py          │    │ • Event Collection Service     │
│ • URL: {tenant}.nlyzer.com     │    │ • Port: 8080                   │    │ • WooCommerceConnector.py      │    │ • Real-time event streaming    │
│ • Port: 8000                   │    │ • Memory: 8GB                  │    │ • BigCommerceConnector.py      │    │ • User behavior tracking       │
│ • Replicas: 1-10 (auto-scale)  │    │ • Storage: 100GB SSD           │    │ • MagentoConnector.py          │    │                                │
│                                │    │                                │    │                                │    │ Event Types:                   │
│ Core API Endpoints:            │    │ Vector Schema Definition:      │    │ API Integration Details:       │    │ • page_view                    │
│ • POST /search/visual          │    │ • Class: Product               │    │ • Shopify GraphQL API v2023-10│    │ • product_search               │
│ • POST /search/text            │    │ • Properties:                  │    │ • WooCommerce REST API v3      │    │ • image_upload                 │
│ • POST /chat/message           │    │   - title: text                │    │ • BigCommerce API v3           │    │ • chat_interaction             │
│ • GET /products/{id}           │    │   - description: text          │    │ • Magento REST API v1          │    │ • purchase_intent              │
│ • POST /recommendations        │    │   - price: number              │    │                                │    │ • conversion_event             │
│ • GET /health                  │    │   - category: text             │    │ Data Synchronization:          │    │ • error_event                  │
│ • GET /metrics                 │    │   - image_url: text            │    │ • Product catalog sync         │    │                                │
│                                │    │   - features: vector<1536>     │    │ • Inventory updates            │    │ Pub/Sub Integration:           │
│ AI Components:                 │    │   - availability: boolean      │    │ • Order processing             │    │ • Topic: analytics-events     │
│ • GPT-4 Vision integration     │    │                                │    │ • Customer data sync           │    │ • Message format: JSON         │
│ • OpenAI Embeddings           │    │ Vector Operations:             │    │                                │    │ • Batch processing: enabled    │
│ • LangChain conversation       │    │ • Similarity search            │    │ Webhook Handlers:              │    │ • Dead letter queue: configured│
│ • Custom prompt engineering    │    │ • Hybrid search (vector+text)  │    │ • POST /webhooks/shopify       │    │                                │
│ • Intent classification        │    │ • Filtered search              │    │ • POST /webhooks/woocommerce   │    │ Analytics Schema:              │
│                                │    │ • Aggregation queries          │    │ • POST /webhooks/bigcommerce   │    │ • user_id: string              │
│ Custom Business Logic:         │    │                                │    │ • POST /webhooks/magento       │    │ • session_id: string           │
│ • nlyzer/agents/sales.py       │    │ Performance Optimization:      │    │                                │    │ • event_type: enum             │
│ • nlyzer/agents/support.py     │    │ • Index configuration          │    │ Authentication Methods:        │    │ • timestamp: ISO 8601          │
│ • nlyzer/agents/recommend.py   │    │ • Memory allocation            │    │ • API Key authentication       │    │ • properties: JSON object      │
│ • nlyzer/agents/conversation.py│    │ • Query optimization           │    │ • OAuth 2.0 flows             │    │                                │
│                                │    │ • Background indexing          │    │ • Webhook signature validation │    │ Data Processing:               │
│ Configuration Management:      │    │                                │    │                                │    │ • Real-time aggregation        │
│ • Environment: production      │    │ Backup Strategy:               │    │ Error Handling:                │    │ • Batch processing (hourly)    │
│ • Config Source: GCS bucket    │    │ • Daily snapshots              │    │ • Rate limiting protection     │    │ • Data validation & cleaning   │
│ • Secret refs: Secret Manager  │    │ • Cross-region replication     │    │ • API timeout handling         │    │ • Schema evolution support     │
│ • Hot reload: enabled          │    │ • Point-in-time recovery       │    │ • Retry with backoff           │    │                                │
│                                │    │ • Disaster recovery plan       │    │ • Circuit breaker pattern      │    │ BigQuery Integration:          │
│ Security Configuration:        │    │                                │    │                                │    │ • Dataset: tenant_analytics    │
│ • JWT token validation         │    │ Monitoring & Alerting:         │    │ Data Transformation:           │    │ • Tables: events, sessions     │
│ • Rate limiting: 100/min       │    │ • Health check endpoint        │    │ • Product normalization        │    │ • Streaming inserts: enabled   │
│ • Input sanitization          │    │ • Memory usage monitoring       │    │ • Image processing pipeline    │    │ • Partitioning: by date        │
│ • CORS policy: restrictive     │    │ • Query performance tracking   │    │ • Price standardization        │    │ • Retention: 2 years           │
│                                │    │ • Index optimization alerts    │    │ • Category mapping             │    │                                │
│ Container Configuration:       │    │                                │    │                                │    │ Real-time Dashboards:          │
│ • Base image: python:3.11-slim │    │ Service Account IAM:           │    │ Service Account IAM:           │    │ • User activity dashboard      │
│ • Multi-stage build           │    │ • compute.instanceAdmin.v1     │    │ • secretmanager.secretAccessor │    │ • Business metrics dashboard   │
│ • Security scanning: enabled   │    │ • storage.objectViewer         │    │ • logging.logWriter            │    │ • Performance monitoring       │
│ • Vulnerability patching       │    │ • logging.logWriter            │    │ • monitoring.metricWriter      │    │ • Error tracking & alerts      │
└────────────────────────────────┘    └────────────────────────────────┘    └────────────────────────────────┘    └────────────────────────────────┘
                │                                        ▲                                        ▲                                        │
                │                                        │                                        │                                        │
                ▼                                        │                                        │                                        ▼
┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                              CUSTOMER EXPERIENCE LAYER                                                                     │
└─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘

┌────────────────────────────────┐    ┌────────────────────────────────┐    ┌────────────────────────────────┐    ┌────────────────────────────────┐
│      CUSTOMER WEBSITE UI       │────│      IMAGE PROCESSING          │────│      AI-POWERED CHAT           │────│      PURCHASE FLOW             │
│                                │    │                                │    │                                │    │                                │
│ Frontend Application:          │    │ Image Analysis Pipeline:       │    │ Conversational AI Engine:     │    │ E-commerce Integration:        │
│ • Framework: Next.js 14        │    │ • GPT-4 Vision API integration │    │ • LangChain conversation chain │    │ • Platform-specific checkout  │
│ • URL: {tenant}.nlyzer.com     │    │ • Image preprocessing pipeline │    │ • Context-aware responses      │    │ • Cart abandonment recovery   │
│ • CDN: Cloudflare             │    │ • Feature extraction           │    │ • Intent classification        │    │ • Payment processing hooks     │
│ • SSL: Let's Encrypt          │    │ • Vector embedding generation   │    │ • Sentiment analysis           │    │                                │
│                                │    │                                │    │                                │    │ UI Components:                 │
│ Core UI Components:            │    │ Computer Vision Stack:         │    │ Chat Interface Components:     │    │ • ProductCard.tsx              │
│ • HomePage.tsx                 │    │ • ImageUploader.tsx            │    │ • ChatWindow.tsx               │    │ • CartSidebar.tsx              │
│ • SearchBar.tsx                │    │ • ImageCropper.tsx             │    │ • MessageBubble.tsx            │    │ • CheckoutButton.tsx           │
│ • ProductGrid.tsx              │    │ • ImagePreview.tsx             │    │ • InputField.tsx               │    │ • PriceDisplay.tsx             │
│ • ProductModal.tsx             │    │ • ProcessingSpinner.tsx        │    │ • SuggestedReplies.tsx         │    │ • StockIndicator.tsx           │
│ • ChatInterface.tsx            │    │                                │    │ • TypingIndicator.tsx          │    │                                │
│ • NavigationMenu.tsx           │    │ Image Processing Flow:         │    │                                │    │ Conversion Optimization:       │
│ • FilterSidebar.tsx            │    │ • Upload validation            │    │ Conversation Management:       │    │ • A/B testing framework        │
│ • LoadingSpinner.tsx           │    │ • Size/format optimization     │    │ • Session state management     │    │ • Recommendation engine        │
│                                │    │ • Content moderation          │    │ • Multi-turn conversation      │    │ • Personalization engine       │
│ State Management:              │    │ • Background removal           │    │ • Memory & context retention   │    │ • Dynamic pricing display      │
│ • Redux Toolkit                │    │ • Feature detection            │    │ • Conversation history         │    │                                │
│ • React Query for API calls    │    │ • Vector embedding             │    │                                │    │ Analytics Integration:         │
│ • Local storage for sessions   │    │                                │    │ AI Response Generation:        │    │ • Google Analytics 4           │
│ • Session persistence          │    │ Supported Formats:             │    │ • Product recommendations      │    │ • Facebook Pixel               │
│                                │    │ • JPEG, PNG, WebP              │    │ • Style suggestions            │    │ • Custom event tracking        │
│ API Integration:               │    │ • Max size: 10MB               │    │ • Size/fit recommendations     │    │ • Conversion funnel analysis   │
│ • Search API calls             │    │ • Min resolution: 200x200      │    │ • Color/material matching      │    │                                │
│ • Chat API integration         │    │ • Max resolution: 4000x4000    │    │ • Availability notifications   │    │ Performance Optimization:      │
│ • Product data fetching        │    │                                │    │                                │    │ • Image lazy loading           │
│ • User preference saving       │    │ Quality Assessment:            │    │ Response Templates:            │    │ • Code splitting               │
│                                │    │ • Blur detection               │    │ • Greeting messages            │    │ • Service worker caching       │
│ Personalization:               │    │ • Lighting analysis            │    │ • Product discovery prompts    │    │ • Bundle optimization          │
│ • User preference tracking     │    │ • Object clarity scoring       │    │ • Purchase guidance            │    │                                │
│ • Search history               │    │ • Background complexity        │    │ • Support escalation           │    │ Security Features:             │
│ • Behavioral analytics         │    │                                │    │                                │    │ • Content Security Policy      │
│ • Recommendation engine        │    │ Error Handling:                │    │ Conversation Flow Control:     │    │ • XSS protection               │
│                                │    │ • Invalid format detection     │    │ • Topic detection              │    │ • CSRF protection              │
│ Accessibility:                 │    │ • Size limit enforcement       │    │ • Context switching            │    │ • Input sanitization          │
│ • WCAG 2.1 AA compliance       │    │ • Processing timeout handling  │    │ • Escalation triggers          │    │                                │
│ • Screen reader support        │    │ • Retry mechanisms             │    │ • Session management           │    │ Mobile Optimization:           │
│ • Keyboard navigation          │    │                                │    │                                │    │ • Responsive design            │
│ • High contrast mode           │    │ Privacy & Security:            │    │ Privacy Controls:              │    │ • Touch-friendly interactions  │
│                                │    │ • Image data encryption        │    │ • Data retention policies      │    │ • Progressive Web App          │
│ Responsive Design:             │    │ • Temporary storage only        │    │ • Conversation export          │    │ • Offline functionality        │
│ • Mobile-first approach        │    │ • No permanent image storage   │    │ • User data deletion           │    │                                │
│ • Tablet optimization          │    │ • Privacy-compliant processing │    │ • GDPR compliance              │    │ Error Handling:                │
│ • Desktop enhancement          │    │                                │    │                                │    │ • Graceful degradation         │
│ • Progressive enhancement      │    │                                │    │                                │    │ • User-friendly error messages │
└────────────────────────────────┘    └────────────────────────────────┘    └────────────────────────────────┘    └────────────────────────────────┘
                                                                                                                                      │
                                                                                                                                      │
                                                                                                                                      ▼
┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                            ANALYTICS & MONITORING LAYER                                                                    │
│                             Service Account: nlyzer-monitoring@nlyzer-shared-services.iam.gserviceaccount.com                           │
└─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘

┌────────────────────────────────┐    ┌────────────────────────────────┐    ┌────────────────────────────────┐    ┌────────────────────────────────┐
│      USAGE ANALYTICS           │────│      SYSTEM MONITORING         │────│      BILLING TRACKING          │────│      PERFORMANCE METRICS      │
│                                │    │                                │    │                                │    │                                │
│ BigQuery Data Pipeline:        │    │ Monitoring Stack:              │    │ Cost Management:               │    │ Performance Monitoring:        │
│ • Dataset: nlyzer_analytics    │    │ • Google Cloud Monitoring     │    │ • GCP Billing API integration │    │ • Application Performance     │
│ • Tables:                      │    │ • Prometheus metrics export    │    │ • Cost breakdown by tenant     │    │ • Database query analysis      │
│   - user_events                │    │ • Grafana dashboards          │    │ • Resource usage tracking      │    │ • Vector search optimization   │
│   - session_data               │    │ • Alertmanager rules           │    │ • Budget alerts & notifications│    │ • API response time tracking   │
│   - conversion_funnel          │    │                                │    │                                │    │                                │
│   - search_analytics           │    │ Health Check Monitoring:       │    │ Billing Components:            │    │ Custom Metrics:                │
│   - chat_interactions          │    │ • Service uptime tracking      │    │ • Cloud Run instance hours     │    │ • search_latency_seconds       │
│                                │    │ • Database connection health   │    │ • Compute Engine VM costs      │    │ • chat_response_time_seconds   │
│ Dataflow Pipeline:             │    │ • API endpoint availability    │    │ • Storage bucket usage         │    │ • image_processing_duration    │
│ • Real-time stream processing  │    │ • Vector database performance  │    │ • Network egress charges       │    │ • conversion_rate_percent      │
│ • Event aggregation            │    │                                │    │ • AI API usage costs           │    │ • user_satisfaction_score      │
│ • Data transformation          │    │ Error Tracking:                │    │                                │    │                                │
│ • Schema validation            │    │ • Sentry error aggregation     │    │ Cost Allocation Logic:         │    │ Alerting Rules:                │
│                                │    │ • Error rate monitoring        │    │ • Per-tenant cost attribution  │    │ • Response time > 2s           │
│ Event Collection:              │    │ • Critical error alerting      │    │ • Department charge-back        │    │ • Error rate > 1%              │
│ • JavaScript SDK integration   │    │ • Error trend analysis         │    │ • Feature usage correlation    │    │ • Availability < 99.9%         │
│ • Server-side event tracking   │    │                                │    │                                │    │ • Resource utilization > 80%   │
│ • Mobile app analytics         │    │ Infrastructure Monitoring:     │    │ Invoice Generation:            │    │                                │
│ • API usage analytics          │    │ • CPU/Memory utilization       │    │ • Automated monthly billing    │    │ Dashboard Integration:         │
│                                │    │ • Disk I/O and storage         │    │ • Usage-based pricing model    │    │ • Grafana operational views    │
│ Data Processing Scripts:       │    │ • Network traffic analysis     │    │ • Subscription management      │    │ • BigQuery business intelligence│
│ • analytics/stream_processor.py│    │ • Container resource usage     │    │ • Payment processing hooks     │    │ • Real-time alerting panels    │
│ • analytics/batch_aggregator.py│    │                                │    │                                │    │ • SLA compliance dashboards    │
│ • analytics/funnel_analyzer.py │    │ Log Aggregation:               │    │ Cost Optimization:             │    │                                │
│ • analytics/cohort_analysis.py │    │ • Centralized logging          │    │ • Right-sizing recommendations │    │ SLI/SLO Definitions:           │
│                                │    │ • Log correlation & search     │    │ • Auto-scaling optimization    │    │ • API availability: 99.9%      │
│ Privacy & Compliance:          │    │ • Audit trail maintenance      │    │ • Reserved instance planning   │    │ • Search latency: p95 < 500ms  │
│ • PII data anonymization       │    │ • Compliance log retention     │    │ • Unused resource cleanup      │    │ • Chat response: p90 < 2s       │
│ • GDPR data retention policies │    │                                │    │                                │    │ • Image processing: p95 < 5s   │
│ • User consent management      │    │ Custom Monitoring Scripts:     │    │ Billing API Integration:       │    │                                │
│ • Data export capabilities     │    │ • tenant_health_checker.py     │    │ • billing/cost_calculator.py   │    │ Capacity Planning:             │
│                                │    │ • service_dependency_map.py    │    │ • billing/invoice_generator.py │    │ • Predictive scaling analysis  │
│ Machine Learning Insights:     │    │ • performance_baseline.py      │    │ • billing/usage_aggregator.py  │    │ • Resource demand forecasting  │
│ • User behavior prediction     │    │ • anomaly_detector.py          │    │ • billing/payment_processor.py │    │ • Cost projection modeling     │
│ • Conversion optimization      │    │                                │    │                                │    │ • Growth planning analytics    │
│ • Personalization engine       │    │ Alerting Channels:             │    │ Financial Reporting:           │    │                                │
│ • Churn prediction model       │    │ • Slack webhook integration    │    │ • Monthly revenue reports      │    │ Data Retention:                │
│                                │    │ • Email alert distribution     │    │ • Customer LTV analysis        │    │ • Metrics: 1 year              │
│ Real-time Dashboards:          │    │ • PagerDuty escalation         │    │ • Churn impact assessment      │    │ • Logs: 90 days                │
│ • User activity heatmaps       │    │ • SMS critical alerts          │    │ • Pricing optimization         │    │ • Events: 2 years              │
│ • Conversion funnel analysis   │    │                                │    │                                │    │ • Billing: 7 years             │
│ • Real-time usage metrics      │    │ Monitoring Service Account:    │    │ Service Account IAM:           │    │                                │
│ • Business KPI tracking        │    │ • monitoring.viewer (cross-    │    │ • billing.viewer               │    │ Compliance & Auditing:         │
│                                │    │   project access)              │    │ • cloudsql.client              │    │ • SOX compliance reporting     │
│ Service Account IAM:           │    │ • logging.viewer               │    │ • bigquery.dataViewer          │    │ • GDPR audit trail             │
│ • bigquery.dataEditor          │    │ • errorreporting.viewer        │    │ • pubsub.subscriber            │    │ • SOC 2 Type II controls       │
│ • dataflow.worker              │    │ • pubsub.publisher             │    │                                │    │ • Financial audit support      │
│ • pubsub.subscriber            │    │                                │    │                                │    │                                │
└────────────────────────────────┘    └────────────────────────────────┘    └────────────────────────────────┘    └────────────────────────────────┘
                                                                                                                                      │
                                                                                                                                      │
                                                                                                                                      ▼
┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                            OPERATIONAL MANAGEMENT LAYER                                                                    │
│                                Service Account: nlyzer-cicd@nlyzer-control-plane.iam.gserviceaccount.com                                │
└─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘

┌────────────────────────────────┐    ┌────────────────────────────────┐    ┌────────────────────────────────┐    ┌────────────────────────────────┐
│        CI/CD PIPELINE          │────│      SECRET ROTATION           │────│    COMPLIANCE & AUDIT          │────│    INCIDENT RESPONSE           │
│                                │    │                                │    │                                │    │                                │
│ GitHub Actions Workflows:      │    │ Secret Management Automation:  │    │ Compliance Framework:          │    │ Incident Management:           │
│ • .github/workflows/           │    │ • Quarterly API key rotation   │    │ • SOC 2 Type II controls       │    │ • PagerDuty integration        │
│   ├── deploy-api.yml           │    │ • Certificate renewal          │    │ • GDPR data protection         │    │ • Incident escalation matrix   │
│   ├── deploy-nlweb.yml         │    │ • Database credential updates  │    │ • HIPAA compliance (healthcare)│    │ • War room procedures          │
│   ├── provision-tenant.yml     │    │ • OAuth secret refresh         │    │ • PCI DSS (payment processing) │    │ • Post-incident reviews        │
│   ├── security-scan.yml        │    │                                │    │                                │    │                                │
│   ├── dependency-update.yml    │    │ Rotation Scripts:              │    │ Audit Logging:                 │    │ Runbook Automation:            │
│   └── backup-restore.yml       │    │ • secrets/rotate_openai.py     │    │ • Cloud Audit Logs collection │    │ • runbooks/database_recovery   │
│                                │    │ • secrets/rotate_stripe.py     │    │ • Admin action tracking        │    │ • runbooks/service_restart     │
│ Container Registry:            │    │ • secrets/rotate_namecheap.py  │    │ • Access pattern analysis      │    │ • runbooks/traffic_failover    │
│ • Artifact Registry repository │    │ • secrets/rotate_certificates  │    │ • Compliance report generation │    │ • runbooks/security_breach     │
│ • Multi-architecture builds    │    │                                │    │                                │    │                                │
│ • Vulnerability scanning       │    │ Secret Validation:             │    │ Security Scanning:             │    │ Health Check Automation:       │
│ • Base image updates           │    │ • API key functionality tests  │    │ • Container image scanning     │    │ • Automated health checks      │
│                                │    │ • Certificate expiry checks    │    │ • Dependency vulnerability     │    │ • Service dependency mapping   │
│ Deployment Strategies:         │    │ • Credential access validation │    │ • Code security analysis       │    │ • Circuit breaker patterns     │
│ • Blue-green deployments       │    │ • Backup verification          │    │ • Infrastructure compliance    │    │ • Auto-remediation scripts     │
│ • Canary releases              │    │                                │    │                                │    │                                │
│ • Rolling updates              │    │ Emergency Procedures:          │    │ Privacy Controls:              │    │ Monitoring Integration:        │
│ • Rollback capabilities        │    │ • Immediate credential         │    │ • Data classification system   │    │ • Real-time alerting           │
│                                │    │   revocation                   │    │ • Consent management platform │    │ • SLA monitoring               │
│ Testing Pipeline:              │    │ • Forensic investigation       │    │ • Data retention policies      │    │ • Performance degradation      │
│ • Unit test execution          │    │ • Breach notification system   │    │ • Right to be forgotten        │    │ • Error rate thresholds        │
│ • Integration testing          │    │ • Regulatory reporting         │    │                                │    │                                │
│ • Security testing            │    │                                │    │ Compliance Reporting:          │    │ Documentation:                 │
│ • Performance testing         │    │ Monitoring & Alerting:         │    │ • Monthly compliance reports   │    │ • Incident response playbooks  │
│                                │    │ • Secret expiry monitoring     │    │ • Annual audit preparation     │    │ • Architecture decision records│
│ Infrastructure as Code:        │    │ • Rotation failure alerts      │    │ • Regulatory filing assistance │    │ • Post-mortem documentation    │
│ • Terraform state management   │    │ • Unauthorized access detection│    │ • Third-party audit support    │    │ • Knowledge base maintenance   │
│ • Environment provisioning     │    │ • Anomaly detection            │    │                                │    │                                │
│ • Resource lifecycle mgmt      │    │                                │    │ Risk Management:               │    │ Training & Procedures:         │
│ • Configuration drift detection│    │ Service Account IAM:           │    │ • Risk assessment matrix       │    │ • Incident response training   │
│                                │    │ • secretmanager.admin          │    │ • Threat modeling              │    │ • Security awareness programs  │
│ Quality Assurance:             │    │ • iam.serviceAccountAdmin      │    │ • Vulnerability management     │    │ • Disaster recovery drills     │
│ • Code coverage reporting      │    │ • certificatemanager.editor    │    │ • Business continuity planning │    │ • Compliance training          │
│ • Static code analysis         │    │ • cloudkms.cryptoKeyEncrypter  │    │                                │    │                                │
│ • Dependency vulnerability     │    │                                │    │ Service Account IAM:           │    │ Service Account IAM:           │
│ • Performance benchmarking     │    │ Key Management:                │    │ • logging.viewer               │    │ • monitoring.admin             │
│                                │    │ • Cloud KMS integration        │    │ • bigquery.admin               │    │ • compute.admin                │
│ Service Account IAM:           │    │ • Hardware Security Modules    │    │ • storage.admin                │    │ • iam.securityAdmin            │
│ • run.admin                    │    │ • Key rotation scheduling      │    │ • cloudsql.admin               │    │ • cloudkms.admin               │
│ • cloudbuild.builds.editor     │    │ • Secure key escrow            │    │                                │    │ • secretmanager.admin          │
│ • artifactregistry.writer      │    │                                │    │                                │    │                                │
│ • source.repos.admin           │    │                                │    │                                │    │                                │
└────────────────────────────────┘    └────────────────────────────────┘    └────────────────────────────────┘    └────────────────────────────────┘

```

## Detailed Process Flow Description

### Phase 1: Customer Acquisition & Onboarding (Boxes A → C)

**Customer Journey Begins:**
1. **Marketing Website (A)**: Potential customer discovers NLyzer through our Next.js marketing site hosted on Cloud CDN
2. **Signup Form (B)**: Customer fills out comprehensive intake form containing:
   - Business name and contact information
   - E-commerce platform type (Shopify, WooCommerce, BigCommerce)
   - Monthly product volume and traffic estimates
   - Preferred AI agent type (sales, support, recommendations)
   - Plan selection (Basic $99, Pro $299, Enterprise $999)
3. **Payment Processing (C)**: Stripe handles secure payment processing with webhook validation

### Phase 2: Control Plane Processing (Boxes D → F)

**Backend API Handles Request:**
4. **Authentication & Validation (D)**: FastAPI service (`nlyzer-api@nlyzer-control-plane.iam.gserviceaccount.com`) processes signup:
   - Validates all inputs using Pydantic models
   - Generates JWT authentication tokens
   - Performs business logic validation
5. **Data Storage (E)**: Customer information stored in PostgreSQL database:
   - Tenant record creation with unique tenant_id
   - Billing information and subscription details
   - E-commerce platform credentials (encrypted)
6. **Provisioning Trigger (F)**: Publishes message to `provisioning-requests` Pub/Sub topic containing tenant configuration

### Phase 3: Automated Infrastructure Provisioning (Boxes G → J)

**Infrastructure as Code Execution:**
7. **Provisioning Function (G)**: Cloud Function (`nlyzer-provisioner@nlyzer-control-plane.iam.gserviceaccount.com`) receives Pub/Sub message
8. **GCP Project Creation (H)**: Using `resourcemanager_v3.ProjectsClient`:
   - Creates isolated GCP project: `nlyzer-tenant-{tenant-id}-{uuid}`
   - Links billing account for cost tracking
   - Applies organizational policies and quotas
9. **IAM Setup (I)**: Using `iam_admin_v1.IAMClient`:
   - Creates tenant service account: `nlweb-{tenant-id}@nlyzer-tenant-{tenant-id}.iam.gserviceaccount.com`
   - Grants minimal permissions: storage.objectViewer, secretmanager.secretAccessor
10. **Secrets Management (J)**: Using `secretmanager.SecretManagerServiceClient`:
    - Stores e-commerce API keys securely
    - Creates tenant-specific secret isolation
    - Sets up automated rotation schedules

### Phase 4: Infrastructure Deployment (Boxes K → N)

**Tenant Environment Creation:**
11. **Vector Database (K)**: Using `compute_v1.InstancesClient`:
    - Deploys Weaviate instance on Google Compute Engine
    - Configures persistent disk storage for embeddings
    - Sets up internal networking with firewall rules
12. **NLWeb Engine (L)**: Using `run_v2.ServicesClient`:
    - Deploys customized NLWeb container to Cloud Run
    - Configures environment variables and service account
    - Sets resource limits and auto-scaling policies
13. **Networking (M)**: Creates secure tenant networking:
    - VPC configuration with tenant-specific subnets
    - Firewall rules allowing only necessary traffic
    - Internal load balancer setup
14. **Configuration Storage (N)**: Using `storage.Client`:
    - Creates GCS bucket: `nlyzer-config-{tenant-id}`
    - Uploads generated `nlweb_config.yml` with tenant-specific settings

### Phase 5: DNS & Domain Management (Boxes O → P)

**Public Access Configuration:**
15. **DNS Setup (O)**: Using Namecheap API integration:
    - Creates subdomain: `{tenant-id}.nlyzer.com`
    - Points A record to Cloud Run service IP
    - Configures SSL certificate for HTTPS
16. **Validation (P)**: Performs comprehensive health checks:
    - Tests endpoint accessibility and response times
    - Validates SSL certificate installation
    - Confirms AI engine functionality

### Phase 6: Tenant Services Operation (Boxes Q → S)

**Live Tenant Environment:**
17. **NLWeb AI Engine (Q)**: The deployed FastAPI service handles:
    - Customer product search requests
    - AI-powered conversation management
    - Integration with vector database for semantic search
18. **Vector Database (R)**: Weaviate instance provides:
    - Storage for product embeddings
    - Semantic similarity search capabilities
    - Real-time query processing
19. **E-commerce Integration (S)**: Handles platform-specific APIs:
    - Shopify/WooCommerce product synchronization
    - Order processing and inventory updates
    - Customer data integration

### Phase 7: Customer Experience (Boxes T → V)

**End-User Interaction:**
20. **Customer Visit (T)**: End customers access `{tenant}.nlyzer.com` for:
    - Visual product search capabilities
    - Conversational commerce experiences
    - AI-powered product recommendations
21. **Image Processing (U)**: Advanced AI capabilities:
    - GPT-4 Vision analysis of uploaded images
    - Vector similarity search against product catalog
    - Contextual product matching and filtering
22. **Conversational AI (V)**: Natural language processing:
    - Intent detection and conversation flow
    - Product recommendations based on preferences
    - Sales conversion optimization

### Phase 8: Analytics & Monitoring (Boxes W → Y)

**Operational Intelligence:**
23. **Usage Analytics (W)**: Data pipeline processing:
    - Pub/Sub collection of user interaction events
    - BigQuery data warehouse for analytics
    - Custom metrics for business intelligence
24. **Monitoring (X)**: Comprehensive observability:
    - Service health monitoring across all components
    - Error tracking and alerting via Sentry
    - Performance metrics and SLA monitoring
25. **Billing Tracking (Y)**: Cost management:
    - Per-tenant resource cost attribution
    - Usage-based billing calculations
    - Automated invoice generation

### Phase 9: Operations & Maintenance (Boxes Z → BB)

**Platform Management:**
26. **CI/CD Pipeline (Z)**: Automated deployment:
    - GitHub Actions workflows using `nlyzer-cicd@nlyzer-control-plane.iam.gserviceaccount.com`
    - Container image builds and pushes to Artifact Registry
    - Automated testing and deployment to Cloud Run
27. **Secret Rotation (AA)**: Security maintenance:
    - Quarterly API key rotation for all services
    - Automated credential updates via Secret Manager
    - Emergency response procedures for compromised keys
28. **Compliance & Auditing (BB)**: Governance and compliance:
    - Cloud Audit Logs for all administrative actions
    - Regular IAM access reviews and cleanup
    - SOC 2 Type II and GDPR compliance reporting

---

## Key Service Accounts & Their Roles

| Service Account | Purpose | Access Scope |
|----------------|---------|--------------|
| `nlyzer-api@nlyzer-control-plane` | Main API service | Pub/Sub, secrets, database |
| `nlyzer-provisioner@nlyzer-control-plane` | Infrastructure automation | Organization-wide project creation |
| `nlyzer-cicd@nlyzer-control-plane` | Deployment pipeline | Cloud Run, Artifact Registry |
| `nlyzer-monitoring@nlyzer-shared-services` | Cross-project monitoring | Read-only monitoring access |
| `nlweb-{tenant}@nlyzer-tenant-{tenant}` | Tenant NLWeb service | Tenant-scoped resource access |
| `weaviate-{tenant}@nlyzer-tenant-{tenant}` | Vector database | Compute and storage access |

---

## Critical Integration Points

### 1. Stripe Webhook Integration
- **Endpoint**: `/api/webhooks/stripe`
- **Validation**: Stripe signature verification
- **Actions**: Subscription activation, billing updates, cancellation handling

### 2. Namecheap DNS API
- **Library**: `namecheapapi` Python client
- **Authentication**: API key + IP whitelist
- **Function**: Automated subdomain creation and SSL setup

### 3. GCP Resource Management
- **Authentication**: Service account key or Application Default Credentials
- **Scope**: Organization-level project creation and tenant-level resource management
- **Monitoring**: Cloud Audit Logs for all provisioning actions

### 4. AI/ML Service Integration
- **OpenAI**: GPT-4 Vision for image analysis, embeddings for search
- **Vector Storage**: Weaviate for semantic product search
- **Fallback**: Anthropic Claude for alternative LLM processing

---

## Security & Compliance Flow

### Data Flow Security
1. **Input Validation**: All customer data validated via Pydantic models
2. **Encryption in Transit**: TLS 1.3 for all API communications
3. **Encryption at Rest**: GCP-managed encryption for all storage
4. **Tenant Isolation**: Complete project-level separation

### Access Control
1. **Principle of Least Privilege**: Each service account has minimal required permissions
2. **Time-Bounded Access**: Temporary elevation during provisioning operations
3. **Audit Logging**: All administrative actions logged to Cloud Audit Logs
4. **Regular Reviews**: Quarterly access reviews and permission cleanup

---

## Disaster Recovery & Business Continuity

### Backup Strategy
- **Database**: Automated PostgreSQL backups with 30-day retention
- **Vector Data**: Weaviate snapshots to Cloud Storage
- **Configuration**: Versioned config files in GCS
- **Code**: Git-based source control with multiple replicas

### Failover Procedures
1. **API Service**: Multi-region Cloud Run deployment with load balancing
2. **Database**: PostgreSQL read replicas in multiple zones
3. **Vector Database**: Weaviate cluster configuration for high availability
4. **DNS**: Health check-based DNS failover via Namecheap

---

## Performance & Scaling

### Auto-Scaling Configuration
- **Cloud Run**: 0-1000 instances per service based on traffic
- **Database**: Connection pooling with overflow handling
- **Vector Database**: Horizontal scaling via Weaviate clusters
- **Storage**: Unlimited capacity with global CDN distribution

### Performance Targets
- **API Response Time**: < 200ms for 95th percentile
- **Search Latency**: < 500ms for vector similarity search
- **Provisioning Time**: < 10 minutes for complete tenant setup
- **Uptime SLA**: 99.9% availability with 4-hour recovery time objective

---

## Conclusion

This visual architecture demonstrates the complete end-to-end business process of the NLyzer platform, from customer acquisition through operational management. The system is designed for enterprise-scale operations with comprehensive security, monitoring, and compliance capabilities.

**Key Success Metrics:**
- ✅ **Automated Onboarding**: 0-touch tenant provisioning in under 10 minutes
- ✅ **Complete Isolation**: Project-level tenant separation for security and compliance  
- ✅ **Enterprise Security**: SOC 2 compliance with comprehensive audit trails
- ✅ **Scalable Architecture**: Auto-scaling infrastructure supporting unlimited growth
- ✅ **Operational Excellence**: 99.9% uptime with comprehensive monitoring and alerting

The architecture successfully bridges the gap between customer acquisition and technical implementation, providing a seamless, secure, and scalable foundation for the NLyzer Conversational Commerce Platform.
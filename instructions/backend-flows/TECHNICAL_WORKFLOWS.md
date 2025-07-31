# NLyzer Technical Workflows - Critical Backend Stories

> 🏗️ **Chief Systems Architect Technical Implementation Blueprint**

## Overview

As Chief Systems Architect for the NLyzer platform, this document provides comprehensive technical workflow mappings for the eight most critical backend stories. Each workflow details the complete system interaction from user action to final response, including all actors, data transformations, technologies used, and references to the relevant documentation.

### **Core Backend Stories**
1. **New B2B Client Onboarding** - The 5-minute deployment experience
2. **End-User Visual Search** - Real-time image-based product discovery
3. **Scheduled Product Catalog Sync** - Keeping inventory fresh across platforms
4. **Monthly Usage-Based Billing** - Automated Stripe billing and invoicing
5. **Concierge Session Handoff** - Premium human expert escalation
6. **NLyzer Intelligence Engine** - ML-powered trends and insights generation
7. **Reporting & Notification Service** - Multi-channel communication system
8. **Feature Flag & Experimentation** - Dynamic feature control and A/B testing

### Workflow Structure
Each workflow is presented as a detailed table showing:
- **Step**: Sequential order of operations
- **Actor**: System component performing the action
- **Action**: Specific operation being performed
- **Data**: Data structures and transformations
- **Technology**: Specific technologies and services used
- **Documentation Reference**: Pointer to relevant documentation in the `/Documentation` library

---

## 1. **New B2B Client Onboarding: The "5-Minute Deployment"**

The most complex and critical workflow - transforming a prospect into an active NLyzer client with fully functional visual search in under 5 minutes.

| Step | Actor | Action | Data | Technology | Documentation Reference |
|------|-------|--------|------|------------|-------------------------|
| 1 | B2B Client Browser | Navigate to signup page | GET /signup | React/Next.js | UX_FLOWS.md - Onboarding |
| 2 | NLyzer Frontend | Display pricing tiers | TierOptions[] | React Components | B2B_DASHBOARD.md - Section 0 |
| 3 | B2B Client Browser | Select plan & submit form | SignupRequest {email, company, tier} | HTTPS POST | UX_FLOWS.md |
| 4 | NLyzer API Gateway | Validate signup data | Pydantic: SignupModel | FastAPI | 02_Core_Technologies/FastAPI/ |
| 5 | NLyzer Auth Service | Create account | User, Store objects | PostgreSQL | 02_Core_Technologies/SQLAlchemy/ |
| 6 | Stripe API | Create customer & subscription | stripe.Customer.create() | Stripe Python SDK | 05_External_Services/Payment/Stripe/ |
| 7 | NLyzer Tenant Service | Provision tenant space | store_id, database schema | PostgreSQL + Redis | 06_Data_Storage/Redis/ |
| 7a | B2B Client Browser | Select e-commerce platform | PlatformSelection {platform: "shopify"} | React dropdown/cards | B2B_DASHBOARD.md - Onboarding |
| 8 | NLyzer Backend | Receive platform choice | PlatformType enum validation | FastAPI endpoint | 02_Core_Technologies/FastAPI/ |
| 9a | Shopify OAuth Service | Initiate Shopify auth flow | OAuth2 redirect URL | Shopify OAuth API | 01_Platform_Integrations/Shopify/ |
| 9b | Custom API Service | Generate API credentials | APIKey object | GCP Secret Manager | 03_Infrastructure/Cloud_Platforms/GCP/ |
| 10 | Product Ingestion | Fetch initial catalog | Product[] via platform API | Platform-specific SDK | 01_Platform_Integrations/{platform}/ |
| 11 | Vector Processing | Generate embeddings | CLIP/GPT-4V embeddings | OpenAI API + Qdrant | 05_External_Services/AI_Libraries/OpenAI/ |
| 12 | Quality Check | Analyze product data | QualityReport {missing_images, etc} | nlyzer/core/product_matcher.py | README.md - Core section |
| 13 | Widget Generator | Create JS snippet | WidgetConfig {store_id, theme} | Jinja2 templates | 04_Development_Tools/Templates/Jinja2/ |
| 14 | Email Service | Send welcome email | WelcomeEmail template | SendGrid/GCP Email | 03_Infrastructure/Cloud_Platforms/GCP/ |
| 15 | Analytics Init | Create dashboard access | DashboardUser permissions | nlyzer/api/admin_dashboard.py | B2B_DASHBOARD.md |

---

## 2. **End-User Visual Search: Real-Time Request**

The core user experience - a shopper uploads an image and receives visually similar products from the client's catalog in real-time.

| Step | Actor | Action | Data | Technology | Documentation Reference |
|------|-------|--------|------|------------|-------------------------|
| 1 | Shopper Browser | Click camera icon | UI interaction | NLyzer Widget JS | UX_FLOWS.md - Maya Chen flow |
| 2 | Widget JS | Capture/upload image | FormData {image: Blob} | HTML5 File API | VISUAL_MOCKUPS.md |
| 3 | CDN | Validate file size/type | image/jpeg, <5MB | CloudFlare/GCP CDN | 03_Infrastructure/Cloud_Platforms/GCP/ |
| 4 | NLyzer API | Authenticate widget | store_id from widget token | FastAPI Depends() | 02_Core_Technologies/FastAPI/ |
| 5 | ConversationManager | Create/retrieve session | conversation_id, Redis cache | nlyzer/core/conversation_manager.py | README.md - Framework section |
| 6 | MultimodalEngine | Process image | ImageFeatures object | nlyzer/core/multimodal_engine.py | 07_Core_Product/NLweb/ |
| 7 | GPT-4V API | Extract style attributes | StyleDNA {colors, patterns, occasion} | OpenAI Vision API | 05_External_Services/AI_Libraries/OpenAI/ |
| 8 | Vector DB | Search embeddings | k-NN search, store_id filter | Qdrant/Pinecone | README.md - Tech Stack |
| 9 | ProductMatcher | Rank results | SimilarityScore[] | nlyzer/core/product_matcher.py | README.md - Implementation |
| 10 | Redis Cache | Cache results | TTL: 5 minutes | Redis SET with expiry | 06_Data_Storage/Redis/ |
| 11 | Response Builder | Format response | SearchResponse {products, confidence} | Pydantic model | 02_Core_Technologies/Pydantic/ |
| 12 | NLyzer API | Publish search event | SearchEvent to Pub/Sub topic | GCP Pub/Sub publish | 03_Infrastructure/Cloud_Platforms/GCP/ |
| 12a | GCP Pub/Sub Topic | Queue analytics events | Topic: analytics_events | Event streaming | 03_Infrastructure/Cloud_Platforms/GCP/ |
| 12b | Analytics Cloud Function | Batch write to database | SearchEvent[] batch insert | Cloud Functions + PostgreSQL | 03_Infrastructure/Cloud_Platforms/GCP/ |
| 13 | Widget JS | Display results | Product carousel UI | React components | UX_FLOWS.md - Results display |

---

## 3. **Scheduled Product Catalog Sync**

Keeping client product data fresh and searchable through automated synchronization with their e-commerce platform.

| Step | Actor | Action | Data | Technology | Documentation Reference |
|------|-------|--------|------|------------|-------------------------|
| 1 | GCP Cloud Scheduler | Trigger sync job | HTTP POST to sync service | Cloud Scheduler → Cloud Run | 03_Infrastructure/Cloud_Platforms/GCP/ |
| 2 | Sync Worker Service | Query active stores | Store[] with sync_enabled=true | Cloud Run (containerized) | 03_Infrastructure/Cloud_Platforms/GCP/ |
| 3 | Platform Router | Route by platform type | PlatformType enum | nlyzer/integrations/ | 01_Platform_Integrations/ |
| 4a | Shopify Client | Fetch product updates | GraphQL: products(updatedAt > last_sync) | Shopify GraphQL | 01_Platform_Integrations/Shopify/ |
| 4b | WooCommerce Client | Fetch via REST API | GET /products?modified_after | WC REST API | 01_Platform_Integrations/WooCommerce/ |
| 5 | Diff Engine | Compare with existing | ProductDiff[] {added, updated, deleted} | nlyzer/core/sync_engine.py | README.md - Architecture |
| 6 | Vector Update Queue | Queue embedding updates | Celery task queue | Celery + Redis | 02_Core_Technologies/Celery/ |
| 7 | Embedding Worker | Process in batches | Batch size: 100 products | OpenAI Batch API | 05_External_Services/AI_Libraries/OpenAI/ |
| 8 | Vector DB | Update/delete vectors | UPSERT operations, store_id partition | Qdrant/Pinecone | README.md - Search section |
| 9 | Sync Logger | Record sync status | SyncLog {products_updated, errors} | PostgreSQL | 02_Core_Technologies/SQLAlchemy/ |
| 10 | Alert Service | Notify on failures | Email/Slack if error_rate > 5% | GCP Monitoring | 08_Monitoring_SRE/SRE_Patterns/ |

---

## 4. **Monthly Usage-Based Billing**

Automated billing cycle that calculates usage, creates invoices, and processes payments through Stripe.

| Step | Actor | Action | Data | Technology | Documentation Reference |
|------|-------|--------|------|------------|-------------------------|
| 1 | GCP Cloud Scheduler | Trigger billing run | 1st of month, 00:00 UTC | Cloud Scheduler | 03_Infrastructure/Cloud_Platforms/GCP/ |
| 2 | Billing Service | Query usage metrics | SearchCount by store_id, date range | PostgreSQL aggregation | 02_Core_Technologies/SQLAlchemy/ |
| 3 | Tier Calculator | Apply pricing rules | $29 base + $0.01/search (Starter) | nlyzer/core/billing.py | README.md - Pricing Tiers |
| 4 | Stripe API | Create usage records | stripe.SubscriptionItem.create_usage_record() | Stripe Python SDK | 05_External_Services/Payment/Stripe/ |
| 5 | Invoice Generator | Calculate totals | Invoice {base_fee, usage_fee, total} | nlyzer/core/invoicing.py | B2B_DASHBOARD.md - Billing section |
| 6 | Stripe API | Create invoice | stripe.Invoice.create() | Stripe Billing | 05_External_Services/Payment/Stripe/ |
| 7 | Webhook Receiver | Handle payment events | StripeWebhook {type: invoice.paid} | nlyzer/api/webhooks.py | 05_External_Services/Payment/Stripe/ |
| 8 | Email Service | Send invoice email | InvoiceEmail template | SendGrid API | B2B_DASHBOARD.md - Weekly Wins |
| 9 | Analytics Update | Update dashboard | Revenue metrics, usage trends | nlyzer/api/admin_dashboard.py | B2B_DASHBOARD.md - Section 6 |
| 10 | Dunning Manager | Handle failures | Payment retry logic | Stripe Dunning | 05_External_Services/Payment/Stripe/ |

---

## 5. **Concierge Session Handoff**

Premium service flow for escalating complex visual searches to human experts when AI confidence is low.

| Step | Actor | Action | Data | Technology | Documentation Reference |
|------|-------|--------|------|------------|-------------------------|
| 1 | Visual Search API | Low confidence detected | confidence < 0.7 threshold | nlyzer/agents/visual_discovery.py | README.md - Agents section |
| 2 | Concierge Router | Check availability | ConciergeAgent[] online status | Redis ZSET (sorted by load) | 06_Data_Storage/Redis/ |
| 3 | Session Manager | Create handoff ticket | HandoffRequest {conversation_id, context} | nlyzer/core/concierge.py | README.md - Premium Services |
| 4 | Queue Manager | Add to priority queue | Redis LIST with priority scoring | Redis LPUSH/RPUSH | 06_Data_Storage/Redis/ |
| 5 | NLyzer Agent Dashboard | Notify next agent | WebSocket notification | Dedicated React web app | B2B_DASHBOARD.md - Concierge |
| 6 | Agent Dashboard Backend | Prepare agent view | SessionContext {images, chat history} | nlyzer/api/concierge_dashboard.py | UX_FLOWS.md - Alexandra Williams |
| 7 | Human Agent | Accept session | Agent claims ticket | PostgreSQL row lock | 02_Core_Technologies/SQLAlchemy/ |
| 8 | Chat Bridge | Enable real-time chat | WebSocket connection | FastAPI + Redis PubSub | 06_Data_Storage/Redis/ |
| 9 | Product Curator | Manual product selection | ExpertPicks[] with notes | nlyzer/api/concierge_tools.py | B2B_DASHBOARD.md - Section 4 |
| 10 | Quality Logger | Record interaction | ConciergeLog for training data | PostgreSQL + S3 | 03_Infrastructure/Cloud_Platforms/GCP/ |
| 11 | Handoff Complete | Return to AI agent | SessionHandback with expert notes | nlyzer/agents/style_psychology.py | README.md - Style Agent |
| 12 | Billing Update | Log premium usage | Usage metric for Enterprise billing | nlyzer/core/billing.py | README.md - Enterprise tier |

---

## 6. **NLyzer Intelligence Engine - Trend & Anomaly Detection**

The data analysis pipeline that powers proactive insights, trend alerts, and inventory opportunities across all B2B dashboards.

| Step | Actor | Action | Data | Technology | Documentation Reference |
|------|-------|--------|------|------------|-------------------------|
| 1 | GCP Cloud Scheduler | Trigger daily analysis | CronJob: 02:00 UTC daily | Cloud Scheduler | 03_Infrastructure/Cloud_Platforms/GCP/ |
| 2 | Analysis Orchestrator | Initiate pipeline | JobConfig {job_id, timestamp, tenants[]} | Cloud Run Jobs | 03_Infrastructure/Cloud_Platforms/GCP/ |
| 3 | BigQuery Service | Execute trend queries | SQL: trend_velocity, failed_searches, patterns | BigQuery ML | 03_Infrastructure/Cloud_Platforms/GCP/ |
| 4 | External Data Collector | Fetch social trends | SocialAPIs {tiktok_trending, instagram_explore} | Social media APIs | 05_External_Services/Social/ |
| 5 | ML Analysis Service | Process anomalies | AnomalyDetection via Vertex AI AutoML | Vertex AI | 03_Infrastructure/Cloud_Platforms/GCP/ |
| 6 | Insight Generator | Create actionable insights | InsightObject[] {type, metric, action, confidence} | nlyzer/intelligence/insight_engine.py | 07_Core_Product/NLweb/ |
| 7 | Trend Scorer | Calculate trend velocity | TrendScore {keyword, velocity, revenue_potential} | Custom ML model | README.md - Intelligence |
| 8 | PostgreSQL Writer | Store insights | TrendAlerts, InventoryOpportunities tables | Batch insert | 02_Core_Technologies/SQLAlchemy/ |
| 9 | Cache Warmer | Update Redis cache | Precomputed insights by store_id | Redis SET with TTL | 06_Data_Storage/Redis/ |
| 10 | Dashboard API | Serve fresh insights | GET /api/insights/{store_id} | FastAPI cached endpoint | B2B_DASHBOARD.md - AI Insights |

### **Intelligence Engine Components**

| Component | Purpose | Technology | Update Frequency |
|-----------|---------|------------|------------------|
| Trend Detector | Identify rising search terms | BigQuery + Time series analysis | Every 4 hours |
| Failed Search Analyzer | Cluster unmatched searches | K-means clustering on embeddings | Daily |
| Social Trend Monitor | Track viral products | TikTok/Instagram APIs + NLP | Real-time stream |
| Revenue Predictor | Estimate opportunity value | Historical conversion data + ML | Daily |
| Anomaly Detector | Flag unusual patterns | Vertex AI Anomaly Detection | Hourly |

---

## 7. **Reporting & Notification Service**

Centralized service handling all scheduled reports, alerts, and multi-channel notifications.

| Step | Actor | Action | Data | Technology | Documentation Reference |
|------|-------|--------|------|------------|-------------------------|
| 1a | Cloud Scheduler (Weekly) | Trigger weekly summary | Event: trigger_weekly_summary | Cloud Scheduler | 03_Infrastructure/Cloud_Platforms/GCP/ |
| 1b | Cloud Scheduler (Alerts) | Check usage thresholds | Event: check_usage_alerts | Cloud Scheduler | 03_Infrastructure/Cloud_Platforms/GCP/ |
| 1c | Real-time Triggers | Detect immediate alerts | Event: viral_trend_detected | Application events | nlyzer/core/events.py |
| 2 | Event Publisher | Publish to topic | NotificationEvent to Pub/Sub | GCP Pub/Sub | 03_Infrastructure/Cloud_Platforms/GCP/ |
| 3 | Notification Router | Route by event type | EventType → Handler mapping | Cloud Function | 03_Infrastructure/Cloud_Platforms/GCP/ |
| 4 | Data Fetcher | Gather required data | ClientMetrics, TrendData from PostgreSQL/BigQuery | Async queries | 02_Core_Technologies/Asyncio/ |
| 5 | Template Engine | Format notification | HTMLEmail, PushNotification, SMSMessage | Jinja2 templates | 04_Development_Tools/Templates/Jinja2/ |
| 6a | Email Service | Send via SendGrid | EmailPayload {to, subject, html, attachments} | SendGrid API | 05_External_Services/Email/ |
| 6b | Push Service | Send mobile push | PushPayload {device_token, title, body, data} | Firebase Cloud Messaging | 03_Infrastructure/Cloud_Platforms/GCP/ |
| 6c | SMS Service | Send text alerts | SMSPayload {phone, message} | Twilio API | 05_External_Services/SMS/ |
| 7 | Delivery Tracker | Log notification status | NotificationLog {sent, opened, clicked} | PostgreSQL | 02_Core_Technologies/SQLAlchemy/ |
| 8 | Retry Manager | Handle failures | Failed notifications → Dead letter queue | Pub/Sub + Cloud Tasks | 03_Infrastructure/Cloud_Platforms/GCP/ |

### **Notification Types & Channels**

| Notification Type | Trigger | Channel | Recipients | Template |
|-------------------|---------|---------|------------|----------|
| Weekly Wins | Monday 9 AM local | Email | B2B clients | B2B_DASHBOARD.md - Weekly Wins |
| Usage Alert | 80% threshold | Email + Push | Account admins | Simple alert template |
| Viral Trend | Real-time detection | Push + Dashboard | James (fashion) | Trend alert with action |
| Payment Failed | Stripe webhook | Email | Billing contact | Payment retry template |
| Sync Error | Sync job failure | Email + Slack | Tech contacts | Technical error report |

---

## 8. **Feature Flag & Experimentation Service**

Enables A/B testing, phased rollouts, and dynamic feature control without code deployments.

| Step | Actor | Action | Data | Technology | Documentation Reference |
|------|-------|--------|------|------------|-------------------------|
| 1 | User Authentication | Login/Session start | UserContext {user_id, store_id, location} | Auth0/Firebase Auth | 02_Core_Technologies/FastAPI/ |
| 2 | Flag Service Client | Request feature flags | FlagRequest {store_id, user_context} | HTTP GET | nlyzer/core/feature_flags.py |
| 3 | Segmentation Engine | Determine user segment | Segment {tier, region, pilot_group} | Business rules engine | README.md - Pricing Tiers |
| 4 | Experiment Allocator | Assign A/B variants | ExperimentAssignment {test_id, variant} | Hash-based assignment | 07_Core_Product/NLweb/ |
| 5 | Flag Store | Fetch active flags | FeatureFlags[] from Redis/PostgreSQL | Redis for speed | 06_Data_Storage/Redis/ |
| 6 | Override Checker | Apply manual overrides | Override {store_id: flags} for pilots | Admin configuration | B2B_DASHBOARD.md - Configuration |
| 7 | Flag Response Builder | Compile final flags | FlagResponse {flags: {}, experiments: {}} | JSON response | 02_Core_Technologies/Pydantic/ |
| 8 | Frontend SDK | Apply flags to UI | Conditional rendering based on flags | React feature flag hooks | UX_FLOWS.md |
| 9 | Backend SDK | Apply flags to logic | Feature-gated code paths | Python decorators | 02_Core_Technologies/Python_Libraries/ |
| 10 | Analytics Logger | Track flag exposure | FlagExposureEvent → Analytics pipeline | Event streaming | Same as workflow #2 |

### **Feature Flag Categories**

| Category | Examples | Control Level | Update Method |
|----------|----------|---------------|---------------|
| Feature Release | visual_search_enabled, concierge_active | Per tenant | Admin dashboard |
| A/B Tests | search_algorithm_variant, ui_layout_test | User percentage | Experiment config |
| Rollout Control | pilot_stores[], regional_availability | Store list/region | Deployment pipeline |
| Capacity Management | max_searches_per_minute, ai_model_version | Global/tenant | Real-time update |
| Emergency Switches | maintenance_mode, disable_feature_x | Global | Instant kill switch |

### **Experimentation Framework**

```python
# Example usage in code
@feature_flag("enhanced_visual_search")
@ab_test("search_algorithm_v2", variants=["control", "ml_enhanced"])
async def visual_search(request: SearchRequest, flags: FeatureFlags):
    if flags.get("enhanced_visual_search"):
        algorithm = flags.get_variant("search_algorithm_v2")
        return await search_engines[algorithm].search(request)
    return await legacy_search(request)
```

---

## Security & Multi-Tenancy Considerations

All workflows implement the following security patterns:

### **Tenant Isolation**
- Every database query includes `WHERE store_id = ?` clause
- Vector database searches filtered by store_id partition
- Redis keys namespaced by store_id (e.g., `store:{store_id}:session:{session_id}`)
- No cross-tenant data access possible

### **Input Validation**
- All API inputs validated using Pydantic models
- File upload size and type restrictions enforced at CDN level
- SQL injection prevention through parameterized queries
- XSS prevention in widget responses

### **Authentication & Authorization**
- Widget requests authenticated via signed JWT tokens
- Admin API endpoints protected with OAuth2 + role checks
- Webhook signatures verified (Stripe, platform webhooks)
- API rate limiting per store_id

### **Secret Management**
- All secrets stored in GCP Secret Manager
- Database credentials rotated automatically
- API keys encrypted at rest
- No secrets in code or environment variables

### **Audit Logging**
- All actions logged with: timestamp, store_id, user_id, action, IP
- Sensitive data (passwords, keys) never logged
- Logs retained for 90 days for compliance
- Real-time alerting for suspicious patterns

### **Data Privacy**
- PII encrypted in database (AES-256)
- GDPR-compliant data retention policies
- Customer data deletion on request
- Anonymous analytics for NLyzer Trends

---

## Production Architecture Components

### **Sync Worker Service**
A dedicated, containerized service for handling product catalog synchronization:

- **Deployment**: GCP Cloud Run (private, VPC-only access)
- **Container**: Docker image with all platform integrations
- **Scaling**: Auto-scales 1-10 instances based on queue depth
- **Endpoint**: `https://sync-worker.nlyzer-internal.com/trigger`
- **Isolation**: Completely separate from main API to prevent resource contention
- **Benefits**: 
  - Long-running sync jobs don't impact API performance
  - Can scale independently based on sync load
  - Easier debugging and monitoring of sync issues

### **NLyzer Agent Dashboard**
A first-class product - dedicated web application for human concierge experts:

- **Technology**: React 18 + TypeScript frontend, FastAPI backend
- **URL**: `https://agents.nlyzer.ai`
- **Features**:
  - Real-time WebSocket notifications for new sessions
  - Split-screen interface: Customer context (left) + Product curation (right)
  - Voice/video chat capabilities for premium consultations
  - Performance metrics and earnings dashboard
  - Training mode for new agents
- **Authentication**: Separate auth system from B2B dashboard
- **Mobile Support**: Responsive design for tablet use during consultations

### **Event-Driven Analytics Architecture**
Decoupled analytics pipeline for ultimate scalability:

```
┌─────────────┐     ┌──────────────┐     ┌─────────────────┐     ┌────────────┐
│ Main API    │────▶│ Pub/Sub Topic │────▶│ Cloud Function  │────▶│ PostgreSQL │
│ (FastAPI)   │     │ analytics_    │     │ (Batch Writer)  │     │ (Analytics)│
└─────────────┘     │ events        │     └─────────────────┘     └────────────┘
                    └──────────────┘              │
                                                  ▼
                                          ┌─────────────────┐
                                          │ BigQuery        │
                                          │ (Data Warehouse)│
                                          └─────────────────┘
```

**Benefits**:
- Main API returns immediately after publishing event
- Cloud Function handles retries and batch optimization
- Can process millions of events without impacting API latency
- Easy to add new subscribers (BigQuery, monitoring, etc.)

### **NLyzer Intelligence Engine**
Advanced ML pipeline for trend detection and business insights:

- **Deployment**: Cloud Run Jobs + Vertex AI
- **Schedule**: Daily analysis at 02:00 UTC, real-time social monitoring
- **Components**:
  - BigQuery ML for trend analysis and SQL-based insights
  - Vertex AI AutoML for anomaly detection
  - Social media API integrations for viral trend tracking
  - Custom Python models for revenue prediction
- **Output**: Populated insights tables that power all B2B dashboards
- **Scale**: Processes millions of search events to surface actionable patterns

### **Reporting & Notification Service**
Multi-channel notification system for all platform communications:

- **Architecture**: Event-driven via Pub/Sub
- **Channels**: Email (SendGrid), Push (FCM), SMS (Twilio), Slack
- **Templates**: Jinja2-based with persona-specific variants
- **Scheduling**: Cloud Scheduler for recurring reports
- **Features**:
  - Timezone-aware delivery
  - Retry logic with dead letter queues
  - Delivery tracking and analytics
  - A/B testing for notification content
- **Scale**: 100K+ notifications daily across all channels

### **Feature Flag & Experimentation Service**
Dynamic configuration system enabling controlled rollouts:

- **Storage**: Redis (hot flags) + PostgreSQL (configuration)
- **SDKs**: Python decorators (backend), React hooks (frontend)
- **Features**:
  - Percentage-based rollouts
  - User segment targeting
  - A/B/n testing framework
  - Emergency kill switches
  - Real-time updates without deployment
- **Integration**: Seamlessly integrated with analytics pipeline
- **Use Cases**: Pilot programs, A/B tests, capacity management

### **Service Communication Matrix**

| Service | Communication Method | Authentication | Rate Limits |
|---------|---------------------|----------------|-------------|
| Main API ↔ Sync Worker | HTTP (internal VPC) | Service account JWT | 100 req/min |
| Main API → Pub/Sub | Async publish | Service account | 10K msg/sec |
| Agent Dashboard ↔ Main API | REST + WebSocket | OAuth2 + JWT | 1K req/min |
| Cloud Functions → Database | Connection pool | Cloud SQL proxy | Batch inserts |
| Intelligence Engine → BigQuery | BigQuery API | Service account | 1K queries/day |
| Notification Service → Channels | Provider APIs | API keys (Secret Manager) | Provider limits |
| Feature Flag Service ↔ Redis | Redis protocol | Internal VPC | 10K req/sec |

---

## Implementation Notes

1. **Async Everything**: All I/O operations use Python's asyncio for maximum performance
2. **Background Tasks**: Heavy operations (embedding generation, sync) use Celery workers
3. **Caching Strategy**: Redis caches with appropriate TTLs for all frequently accessed data
4. **Error Handling**: Every workflow includes rollback procedures and error notifications
5. **Monitoring**: Prometheus metrics exported for all critical paths
6. **Testing**: Each workflow has comprehensive unit and integration tests
7. **Service Isolation**: Each major component runs as independent service for reliability
8. **Event-Driven**: Analytics and non-critical operations use Pub/Sub for decoupling

This production-grade architectural blueprint serves as the authoritative guide for implementing NLyzer's core backend functionality with enterprise-level scalability and reliability.
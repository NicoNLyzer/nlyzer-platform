# CEO Credential Collection Guide
## Step-by-Step Instructions for Obtaining All NLyzer Platform API Keys

> **Purpose**: This guide provides click-by-click instructions with exact URLs for obtaining all 91 MVP environment variables needed to launch NLyzer.
> **Time Required**: 3-4 hours total
> **Prerequisites**: Corporate credit card for paid services

---

## Table of Contents
1. [Google Cloud Platform (15 variables)](#1-google-cloud-platform)
2. [Stripe Payments (6 variables)](#2-stripe-payments)
3. [OpenAI API (5 variables)](#3-openai-api)
4. [Database Services (7 variables)](#4-database-services)
5. [SendGrid Email (3 variables)](#5-sendgrid-email)
6. [Sentry Monitoring (3 variables)](#6-sentry-monitoring)
7. [OAuth Providers (4 variables)](#7-oauth-providers)
8. [Namecheap Domain (5 variables)](#8-namecheap-domain)
9. [Application Secrets (4 variables)](#9-application-secrets)

---

## 1. Google Cloud Platform
**URL**: https://console.cloud.google.com
**Time**: 45 minutes
**Cost**: Free tier available, ~$300 credit for new accounts

### Step 1: Create GCP Account
1. Go to https://cloud.google.com/free
2. Click **"Get started for free"** (blue button, top right)
3. Sign in with your Google account or create one
4. Enter billing information (won't be charged during free trial)
5. Accept terms and click **"Start my free trial"**

### Step 2: Create New Project
1. Go to https://console.cloud.google.com
2. Click the project dropdown (top navigation bar, next to "Google Cloud")
3. Click **"NEW PROJECT"** (top right of modal)
4. Project name: `nlyzer-production`
5. Click **"CREATE"**
6. Wait 30 seconds for creation
7. **SAVE**: `GCP_PROJECT_ID` = The ID shown under project name (e.g., `nlyzer-production-123456`)

### Step 3: Enable Required APIs
1. Go to https://console.cloud.google.com/apis/library
2. Search and enable each of these (click API → click **"ENABLE"**):
   - Cloud Run API
   - Secret Manager API
   - Cloud Storage API
   - Artifact Registry API
   - Cloud Build API
   - Pub/Sub API

### Step 4: Create Service Account
1. Go to https://console.cloud.google.com/iam-admin/serviceaccounts
2. Click **"+ CREATE SERVICE ACCOUNT"** (top of page)
3. Service account name: `nlyzer-dev-sa`
4. Click **"CREATE AND CONTINUE"**
5. Role: Select **"Owner"** (for dev only, restrict in production)
6. Click **"CONTINUE"** → **"DONE"**
7. Click on the created service account email
8. Go to **"KEYS"** tab
9. Click **"ADD KEY"** → **"Create new key"**
10. Choose **"JSON"** → **"CREATE"**
11. **SAVE**: Downloaded file path as `GOOGLE_APPLICATION_CREDENTIALS`

### Step 5: Create Storage Buckets
1. Go to https://console.cloud.google.com/storage/browser
2. Click **"+ CREATE"** (top of page)
3. Bucket name: `nlyzer-storage-dev`
4. Location: **"us-central1"**
5. Storage class: **"Standard"**
6. Click **"CREATE"**
7. Repeat for bucket: `nlyzer-configs-dev`
8. **SAVE**: 
   - `GCS_BUCKET_NAME` = `nlyzer-storage-dev`
   - `GCS_CONFIG_BUCKET` = `nlyzer-configs-dev`

### Step 6: Set Up Artifact Registry
1. Go to https://console.cloud.google.com/artifacts
2. Click **"+ CREATE REPOSITORY"**
3. Name: `nlyzer-images`
4. Format: **"Docker"**
5. Location: **"us-central1"**
6. Click **"CREATE"**
7. **SAVE**:
   - `ARTIFACT_REGISTRY_REPO` = `nlyzer-images`
   - `ARTIFACT_REGISTRY_LOCATION` = `us-central1`

### Variables Collected:
```env
GCP_PROJECT_ID=nlyzer-production-123456
GCP_REGION=us-central1
GCP_ZONE=us-central1-a
GOOGLE_APPLICATION_CREDENTIALS=/path/to/downloaded-key.json
GCS_BUCKET_NAME=nlyzer-storage-dev
GCS_CONFIG_BUCKET=nlyzer-configs-dev
GCP_SECRET_PROJECT=nlyzer-production-123456
CLOUD_RUN_SERVICE_NAME=nlyzer-api
CLOUD_RUN_REGION=us-central1
ARTIFACT_REGISTRY_REPO=nlyzer-images
ARTIFACT_REGISTRY_LOCATION=us-central1
```

---

## 2. Stripe Payments
**URL**: https://dashboard.stripe.com
**Time**: 30 minutes
**Cost**: Free to start, 2.9% + 30¢ per transaction

### Step 1: Create Stripe Account
1. Go to https://dashboard.stripe.com/register
2. Enter email and create password
3. Verify email (check inbox)
4. Fill business details:
   - Business name: `NLyzer`
   - Country: Your country
   - Business type: `Company`

### Step 2: Get API Keys (Test Mode)
1. Go to https://dashboard.stripe.com/test/apikeys
2. **SAVE** from "Standard keys" section:
   - `STRIPE_PUBLISHABLE_KEY` = The key starting with `pk_test_`
   - `STRIPE_SECRET_KEY` = Click **"Reveal test key"** → Copy key starting with `sk_test_`

### Step 3: Create Products and Prices
1. Go to https://dashboard.stripe.com/test/products
2. Click **"+ Add product"**
3. Create **Basic Plan**:
   - Name: `NLyzer Basic`
   - Pricing: `$99/month`
   - Click **"Save product"**
4. Click on the created product
5. **SAVE**: `STRIPE_PRICE_ID_BASIC` = The price ID (e.g., `price_1ABC...`)
6. Repeat for:
   - **Pro Plan**: `$299/month` → `STRIPE_PRICE_ID_PRO`
   - **Enterprise Plan**: `$999/month` → `STRIPE_PRICE_ID_ENTERPRISE`

### Step 4: Set Up Webhook
1. Go to https://dashboard.stripe.com/test/webhooks
2. Click **"+ Add endpoint"**
3. Endpoint URL: `https://your-domain.com/api/v1/stripe/webhook` (update later)
4. Events: Select **"Select all events"** (refine later)
5. Click **"Add endpoint"**
6. **SAVE**: `STRIPE_WEBHOOK_SECRET` = The signing secret (click **"Reveal"**)

### Variables Collected:
```env
STRIPE_SECRET_KEY=sk_test_51ABC...
STRIPE_PUBLISHABLE_KEY=pk_test_51ABC...
STRIPE_WEBHOOK_SECRET=whsec_ABC123...
STRIPE_PRICE_ID_BASIC=price_1ABC...
STRIPE_PRICE_ID_PRO=price_1DEF...
STRIPE_PRICE_ID_ENTERPRISE=price_1GHI...
```

---

## 3. OpenAI API
**URL**: https://platform.openai.com
**Time**: 15 minutes
**Cost**: Pay-as-you-go, ~$0.03 per 1K tokens

### Step 1: Create OpenAI Account
1. Go to https://platform.openai.com/signup
2. Sign up with email or Google
3. Verify phone number
4. Complete onboarding

### Step 2: Add Payment Method
1. Go to https://platform.openai.com/settings/organization/billing/overview
2. Click **"Add payment details"**
3. Enter credit card information
4. Set initial credit: `$50` (recommended for testing)

### Step 3: Create API Key
1. Go to https://platform.openai.com/api-keys
2. Click **"+ Create new secret key"**
3. Name: `NLyzer Development`
4. Permissions: **"All"**
5. Click **"Create secret key"**
6. **SAVE IMMEDIATELY**: `OPENAI_API_KEY` = The key shown (starts with `sk-`)
7. ⚠️ **Warning**: You cannot view this key again after closing

### Step 4: Configure Settings
1. Go to https://platform.openai.com/settings/organization/limits
2. Set monthly budget: `$100` (adjust as needed)
3. Set rate limits (optional but recommended)

### Variables Collected:
```env
OPENAI_API_KEY=sk-proj-ABC123...
OPENAI_MODEL=gpt-4
OPENAI_EMBEDDING_MODEL=text-embedding-3-small
OPENAI_MAX_TOKENS=2000
OPENAI_TEMPERATURE=0.7
```

---

## 4. Database Services
**Time**: 20 minutes for local setup
**Cost**: Free for development

### PostgreSQL (Local Docker)
```bash
# These are default values for local development
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/nlyzer_db
DATABASE_POOL_SIZE=20
DATABASE_MAX_OVERFLOW=10
```

### Redis (Local Docker)
```bash
# These are default values for local development
REDIS_URL=redis://localhost:6379/0
REDIS_PASSWORD=
REDIS_SSL=false
```

### Qdrant (Local Docker)
```bash
# These are default values for local development
QDRANT_URL=http://localhost:6333
QDRANT_API_KEY=
```

**Note**: For production, replace with managed services:
- PostgreSQL: Use Cloud SQL (https://console.cloud.google.com/sql)
- Redis: Use Memorystore (https://console.cloud.google.com/memorystore)
- Qdrant: Use Qdrant Cloud (https://cloud.qdrant.io)

---

## 5. SendGrid Email
**URL**: https://app.sendgrid.com
**Time**: 20 minutes
**Cost**: Free for 100 emails/day

### Step 1: Create SendGrid Account
1. Go to https://signup.sendgrid.com
2. Fill registration form:
   - Email: Your email
   - Password: Create strong password
   - Company: `NLyzer`
3. Verify email address

### Step 2: Complete Sender Authentication
1. Go to https://app.sendgrid.com/settings/sender_auth
2. Click **"Authenticate Your Domain"**
3. DNS host: Select your provider (e.g., "Namecheap")
4. Domain: `nlyzer.com`
5. Follow DNS setup instructions (coordinate with Namecheap setup)

### Step 3: Create API Key
1. Go to https://app.sendgrid.com/settings/api_keys
2. Click **"Create API Key"**
3. API Key Name: `NLyzer Production`
4. API Key Permissions: **"Full Access"**
5. Click **"Create & View"**
6. **SAVE**: `SENDGRID_API_KEY` = The key shown (starts with `SG.`)

### Step 4: Set Up Sender
1. Go to https://app.sendgrid.com/settings/sender_auth/senders
2. Click **"Create New Sender"**
3. Fill details:
   - From Name: `NLyzer Platform`
   - From Email: `noreply@nlyzer.com`
4. Verify sender email

### Variables Collected:
```env
SENDGRID_API_KEY=SG.ABC123...
SENDGRID_FROM_EMAIL=noreply@nlyzer.com
SENDGRID_FROM_NAME=NLyzer Platform
```

---

## 6. Sentry Monitoring
**URL**: https://sentry.io
**Time**: 15 minutes
**Cost**: Free for 5K errors/month

### Step 1: Create Sentry Account
1. Go to https://sentry.io/signup
2. Sign up with email or Google
3. Organization name: `NLyzer`
4. Choose: **"I'm working on my own project"**

### Step 2: Create Project
1. Platform: Select **"Python"**
2. Alert frequency: **"Alert me on every new issue"**
3. Project name: `nlyzer-api`
4. Team: `#nlyzer`
5. Click **"Create Project"**

### Step 3: Get DSN
1. Go to https://sentry.io/settings/nlyzer/projects/nlyzer-api/keys/
2. **SAVE**: `SENTRY_DSN` = The DSN shown (starts with `https://`)

### Variables Collected:
```env
SENTRY_DSN=https://abc123@o123456.ingest.sentry.io/123456
SENTRY_ENVIRONMENT=development
SENTRY_TRACES_SAMPLE_RATE=0.1
```

---

## 7. OAuth Providers

### GitHub OAuth
1. Go to https://github.com/settings/developers
2. Click **"New OAuth App"**
3. Fill details:
   - Application name: `NLyzer`
   - Homepage URL: `https://nlyzer.com`
   - Authorization callback URL: `https://api.nlyzer.com/auth/github/callback`
4. Click **"Register application"**
5. **SAVE**:
   - `GITHUB_CLIENT_ID` = The Client ID shown
   - `GITHUB_CLIENT_SECRET` = Click **"Generate a new client secret"** → Copy

### Google OAuth
1. Go to https://console.cloud.google.com/apis/credentials
2. Click **"+ CREATE CREDENTIALS"** → **"OAuth client ID"**
3. Application type: **"Web application"**
4. Name: `NLyzer Web`
5. Authorized redirect URIs: Add `https://api.nlyzer.com/auth/google/callback`
6. Click **"CREATE"**
7. **SAVE**:
   - `GOOGLE_CLIENT_ID` = The Client ID shown
   - `GOOGLE_CLIENT_SECRET` = The Client Secret shown

### Variables Collected:
```env
GITHUB_CLIENT_ID=Ov23liABC...
GITHUB_CLIENT_SECRET=abc123...
GOOGLE_CLIENT_ID=123456-abc.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=GOCSPX-ABC...
```

---

## 8. Namecheap Domain
**URL**: https://www.namecheap.com
**Time**: 20 minutes
**Cost**: ~$10/year for .com domain

### Step 1: Purchase Domain
1. Go to https://www.namecheap.com
2. Search for `nlyzer.com`
3. Add to cart and purchase
4. Create account if needed

### Step 2: Enable API Access
1. Go to https://ap.www.namecheap.com/settings/tools/apiaccess/
2. Toggle **"API Access"** to ON
3. Whitelist your IP:
   - Find your IP: Go to https://whatismyipaddress.com
   - Add this IP to whitelist
4. **SAVE** the credentials shown

### Step 3: Get API Credentials
1. Go to https://ap.www.namecheap.com/settings/tools/apiaccess/whitelisted-ips
2. **SAVE**:
   - `NAMECHEAP_API_USER` = Your Namecheap username
   - `NAMECHEAP_API_KEY` = The API key shown
   - `NAMECHEAP_USERNAME` = Your Namecheap username
   - `NAMECHEAP_CLIENT_IP` = Your whitelisted IP

### Variables Collected:
```env
NAMECHEAP_API_USER=yourncusername
NAMECHEAP_API_KEY=abc123...
NAMECHEAP_USERNAME=yourncusername
NAMECHEAP_CLIENT_IP=123.456.789.0
NAMECHEAP_SANDBOX_MODE=false
NAMECHEAP_BASE_DOMAIN=nlyzer.com
```

---

## 9. Application Secrets
**Generate locally - DO NOT use online generators**

### Generate Secret Key (Terminal/Command Prompt)
```bash
# On Mac/Linux:
python3 -c "import secrets; print(secrets.token_urlsafe(32))"

# On Windows:
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

### Variables to Generate:
```env
SECRET_KEY=<output from command above>
JWT_ALGORITHM=HS256
JWT_EXPIRATION_HOURS=24
SESSION_SECRET_KEY=<run command again for different value>
SESSION_EXPIRE_MINUTES=1440
```

---

## Final Checklist

### Core Services (Must Have)
- [ ] GCP Project Created
- [ ] GCP Service Account Key Downloaded
- [ ] Stripe Account with Products
- [ ] OpenAI API Key
- [ ] SendGrid API Key
- [ ] Generated Secret Keys

### Optional for MVP Launch
- [ ] Sentry (can add later)
- [ ] OAuth Providers (can use email/password initially)
- [ ] Namecheap API (can configure DNS manually)

### Production Readiness
- [ ] All test keys replaced with production keys
- [ ] Stripe switched to live mode
- [ ] GCP billing alerts configured
- [ ] OpenAI usage limits set
- [ ] Domain DNS configured

---

## Next Steps

1. **Save all credentials** in a secure password manager (1Password, Bitwarden, etc.)
2. **Create `.env` file** from `.env.example` and populate with collected values
3. **Test connections** using the verification script: `python scripts/verify_credentials.py`
4. **Never commit** the `.env` file to Git (already in .gitignore)

## Support Contacts

- **GCP Support**: https://cloud.google.com/support
- **Stripe Support**: support@stripe.com
- **OpenAI Support**: https://help.openai.com
- **SendGrid Support**: https://support.sendgrid.com

---

**Time Estimate Summary**:
- Google Cloud Platform: 45 minutes
- Stripe: 30 minutes
- OpenAI: 15 minutes
- SendGrid: 20 minutes
- Sentry: 15 minutes
- OAuth Providers: 20 minutes
- Namecheap: 20 minutes
- Secret Generation: 5 minutes

**Total: ~3 hours**

---

*Document Version: 1.0*
*Last Updated: 2025-08-03*
*Next Review: After first deployment*
# The Unified Architectural Blueprint for NLyzer (Definitive, Hardened Master Plan)

> This is the definitive, unredacted, and fully detailed Unified Architectural Blueprint. It is a complete, self-contained document integrating all sections and their subsections with the highest level of specificity. It is the master plan for implementation.

## 1. The Deployment Strategy

### #### Technical Explanation

**Foundational Features (from repository analysis):**
The open-source NLWeb project is designed for containerization, defined by its root Dockerfile and docker-compose.yml. The application entrypoint specified in the Dockerfile is CMD ["python", "-m", "nlweb.main"], which starts a FastAPI server. Its local deployment configuration, as detailed in docker-compose.yml, relies on environment variables (e.g., NLWEB_CONFIG_PATH, WEAVIATE_URL, OPENAI_API_KEY) to manage its runtime settings.

**NLyzer's GCP Architecture:**
Our managed service will forgo docker-compose in favor of a scalable, single-tenant GCP architecture. Each client deployment will consist of the following resources provisioned within a dedicated GCP Project to ensure absolute billing and resource isolation:

- **Compute:** The NLWeb Dockerfile will be used to build a container image, which will be stored and versioned in Google Artifact Registry. For each tenant, this image will be deployed as a dedicated GCP Cloud Run service. This serverless model provides perfect process isolation, automatic scaling (including to zero), and managed infrastructure, making it ideal for our single-tenant web application workload.

- **Database:** Each tenant requires an isolated vector database. We will deploy the official Weaviate Docker image to a dedicated GCP Compute Engine (GCE) instance, provisioned from a pre-configured instance template. The GCE instance's persistent disk will store the Weaviate data, ensuring persistence across restarts.

- **Orchestration:** A central GCP Cloud Function, triggered by a Pub/Sub message, will act as our "Provisioning Robot," orchestrating the entire setup as detailed in the subsequent sections.

### #### Simple Explanation

We deploy NLWeb for each client using GCP Cloud Run, which gives them a private and secure mini-server. Each client also gets their own private Weaviate database. We automate the entire setup using a master robot (a GCP Cloud Function) that builds a new, dedicated environment for each client.

## 2. The Automated Provisioning Handshake

This workflow details the event-driven process that securely translates a customer onboarding event into a live, configured NLWeb instance, solving the critical "chicken-and-egg" problem of configuration dependency.

### 2.1. The Waiting Mechanism

#### #### Technical Explanation

The generic NLWeb application waits dormantly as a container image, not as a running instance, to eliminate costs for unconfigured tenants.

**The Dormant Blueprint:** The "waiting instance" is our generic NLWeb container image, built from the project's Dockerfile and stored by tag in Google Artifact Registry. It is functionally inert and incurs no cost while stored.

**Resilient Startup Logic (Proposed Code Change):** The application's entrypoint, nlweb/main.py, must be modified to handle a missing or incomplete configuration gracefully. The main startup block will be wrapped in a try/except structure to prevent crash-looping in a non-obvious way.

```python
# Proposed change inside nlweb/main.py
import sys
import os

def initialize_application():
    try:
        # Step 1: Attempt to load config from the GCS path specified in the environment.
        config_path = os.environ.get("NLWEB_CONFIG_PATH")
        if not config_path:
            raise ValueError("NLWEB_CONFIG_PATH environment variable not set.")
        config = load_config_from_gcs(config_path) # Assumes a helper function.
        
        # Step 2: Attempt to connect to the Weaviate DB specified in the environment.
        weaviate_url = os.environ.get("WEAVIATE_URL")
        if not weaviate_url:
            raise ValueError("WEAVIATE_URL environment variable not set.")
        weaviate_client = connect_to_weaviate(weaviate_url)
        
    except Exception as e:
        # If config or DB is not ready, log the specific error and exit with a non-zero status code.
        print(f"FATAL: Application startup failed: {e}. Configuration is not ready. Exiting.")
        sys.exit(1) # This specific exit code is critical for Cloud Run's health checks.
        
    # ... proceed with normal application startup, attaching clients and config to the app state.```

**Cloud Run's Role:** This non-zero exit code will cause the Cloud Run startup health check to fail. Cloud Run's managed nature will automatically try to restart the container on an exponential backoff schedule, creating a managed, cost-effective "waiting" loop until the configuration dependencies are met.

#### #### Simple Explanation

The "waiting instance" is like a flat-pack IKEA furniture kit (our generic NLWeb software) stored in our warehouse (Google Artifact Registry). It remains in the warehouse, costing us nothing, until an order comes in. We don't build the furniture and have it "wait" for instructions; we wait for the instructions before we even start building.

### 2.2. The Configuration Generation

#### #### Technical Explanation

The process is triggered by the Provisioning Cloud Function consuming a message from a GCP Pub/Sub topic.

**Trigger:** The Provisioning Cloud Function is configured with a Pub/Sub trigger, subscribed to the provisioning-requests topic. It activates upon receiving a message with a defined schema.

**Secure Credential Storage:** The function's first action is to extract sensitive data from the message payload (e.g., credentials.shopify_access_token) and write it directly to Google Secret Manager. It will create a new secret with a predictable name, such as tenant-{tenant_id}-shopify-token.

**YAML Generation (Repo-Aware):** The function programmatically generates the nlweb_config.yml file as a string. The structure of this YAML will precisely match the schemas expected by the factory patterns in nlweb/data_loaders/__init__.py and nlweb/tools/__init__.py. For any sensitive value, it will embed the full resource path to the secret in Secret Manager, not the raw secret itself.

**Upload to GCS:** The function creates a new, dedicated GCS bucket (e.g., nlyzer-config-{tenant_id}) and uploads the generated nlweb_config.yml string as a file object.

#### #### Simple Explanation

When a work order arrives in our system, our master robot (the Cloud Function) gets to work. Its first job is to take the client's secret password (their API key) and lock it in a secure digital vault (Secret Manager). Then, it writes the assembly instructions (config.yml) for the client's server. Instead of writing the secret password on the instructions, it just writes the location of the vault where the password is kept. Finally, it places this instruction sheet into a private, labeled folder (Cloud Storage) just for that client.

### 2.3. The Secure Application

#### #### Technical Explanation

The configuration is securely applied by deploying the Cloud Run service with a least-privilege identity and environment variables pointing to the configuration resources.

**IAM & Service Accounts:** The Provisioning Function creates a dedicated GCP Service Account for the tenant (e.g., sa-{tenant_id}@...). It then applies fine-grained IAM bindings to this service account, granting it roles/storage.objectViewer on the specific GCS config bucket and roles/secretmanager.secretAccessor on the specific secret versions created in the previous step.

**Secret Resolution (Proposed Code Change):** We will add a helper function, likely in a new nlweb/gcp_utils.py module, to recursively traverse the loaded YAML config dictionary and resolve any string values that match the Secret Manager path format.

```python
# Proposed function in nlweb/gcp_utils.py
from google.cloud import secretmanager

def resolve_secrets_in_config(config: dict) -> dict:
    client = secretmanager.SecretManagerServiceClient()
    for key, value in config.items():
        if isinstance(value, dict):
            resolve_secrets_in_config(value)
        elif isinstance(value, str) and value.startswith("projects/"):
            try:
                response = client.access_secret_version(name=value)
                config[key] = response.payload.data.decode("UTF-8")
            except Exception as e:
                print(f"Failed to resolve secret: {value}. Error: {e}")
                raise
    return config
```

**Cloud Run Deployment:** The Provisioning Function programmatically defines and deploys a new Cloud Run service. The service definition will specify: the Artifact Registry URI of the generic NLWeb image; the identity of the tenant's dedicated Service Account; and the necessary environment variables (NLWEB_CONFIG_PATH=gs://..., WEAVIATE_URL=http://..., TENANT_ID=...).

**The Handshake:** On startup, the Cloud Run instance, acting as its assigned Service Account, has the IAM permissions to fetch the nlweb_config.yml from GCS. The NLWeb application code then parses this YAML and uses the resolve_secrets_in_config function to fetch the sensitive values directly from Secret Manager into memory, completing the secure configuration load.

#### #### Simple Explanation

The robot now assembles the client's personal server (Cloud Run) using the flat-pack kit from the warehouse. It attaches a note to the server that says, "Your instruction sheet is in this private folder." Crucially, it also gives the server a special keycard (a Service Account) that only works on that specific folder and the specific digital vault location mentioned in the instructions. When the server turns on for the first time, it reads the note, uses its keycard to get the instruction sheet, sees the vault location, and uses its keycard again to retrieve the secret password from the vault.

### 2.4. The First Data Ingestion

#### #### Technical Explanation

An explicit, auditable API call triggers the initial data synchronization after the service is confirmed healthy.

**Sync Endpoint (Proposed Code Change):** We will add a new, system-level endpoint to the FastAPI application in nlweb/main.py. This endpoint will be protected by IAM to ensure it can only be invoked by our Provisioning Function's identity.

```python
# Proposed endpoint in nlweb/main.py
from fastapi import FastAPI, Request, Depends
from some_auth_library import require_iam_permission # Pseudocode for IAM check

app = FastAPI()
# ...
@app.post("/v1/system/trigger-initial-sync", dependencies=[Depends(require_iam_permission("run.invoker"))])
def trigger_sync(request: Request):
    # Assuming loaders have been initialized and attached to the app state
    for loader_name, loader_instance in app.state.data_loaders.items():
        print(f"Triggering initial sync for loader: {loader_name}")
        # Consider running this in a background task for long-running jobs
        loader_instance.load() # Calls the .load() method on ShopifyLoader, etc.
    return {"status": "Initial sync process initiated for all configured data loaders."}
```

**The Final Call:** After the Provisioning Function successfully deploys the Cloud Run service and its health checks pass, the function's final action is to make an authenticated POST request to this /v1/system/trigger-initial-sync endpoint on the newly created Cloud Run service's URL.

#### #### Simple Explanation

Once the robot has built the server and confirmed it turned on correctly, it makes one final, authoritative call: "Start your first big data sync now!" This command tells the newly live server to immediately start reading all the product data from the client's Shopify store. This ensures the server is fully stocked with data and ready for the client's first query.

### 2.5. Orchestration Plane Security

#### #### Technical Explanation

The Provisioning Cloud Function is the most privileged component in our infrastructure and must be treated as a high-value target. The following hardening strategies are mandatory.

**Trigger Security:** The Provisioning Cloud Function will be configured to allow "private" invocations only, requiring authentication. We will set its ingress settings to "Allow internal traffic only" and its trigger to be the private provisioning-requests Pub/Sub topic. The NLyzer API backend will publish to this topic, but no external service can.

**Principle of Least Privilege:** The service account assigned to the Provisioning Function itself will be granted the following, highly specific IAM roles. It will not be granted basic roles like Editor or Owner.

roles/resourcemanager.projectCreator: To create the dedicated tenant GCP Project.

roles/billing.user: To link the new project to our master billing account.

roles/iam.serviceAccountAdmin: To create, get, and set IAM policies on new tenant service accounts.

roles/run.admin: To deploy and manage Cloud Run services within the tenant project.

roles/compute.admin: To create GCE instances, disks, and firewall rules for Weaviate.

roles/storage.admin: To create GCS buckets and upload the configuration file.

roles/secretmanager.admin: To create and manage secrets for tenant credentials.

roles/bigquery.dataEditor: To create the authorized BigQuery view for the tenant's analytics.

**Code Security:** The CI/CD pipeline for the Provisioning Function will include mandatory security gates:

- **Mandatory Code Reviews:** A GitHub branch protection rule will require at least one approval from a designated senior engineer before code can be merged into the main branch.

- **Static Analysis Security Testing (SAST):** We will integrate GitHub CodeQL into the pipeline. This will automatically scan the function's code for common security vulnerabilities on every pull request. A failed scan will block the merge.

- **Dependency Scanning:** We will use GitHub's Dependabot to automatically scan our requirements.txt for known vulnerabilities and create pull requests to patch them.

#### #### Simple Explanation

Our master robot (the Provisioning Function) is very powerful, so we're putting it in a high-security room.

**Trigger Security:** The robot only responds to orders from a private, internal mailbox. No one from the outside can send it instructions.

- **Least Privilege:** Instead of a master key to the whole building, the robot has a keychain with specific keys. One key only creates new project folders, another only creates servers, and so on. If one key is stolen, the damage is limited.

- **Code Security:** Before we ever update the robot's programming, the new code must pass a mandatory inspection. An automated security scanner checks for flaws, and a senior engineer must personally sign off on the changes.

## 3. The Client Onboarding & Website Backend Blueprint

### 3.1. The Website Hosting Strategy

#### #### Technical Explanation

**Hosting Service:** GCP Cloud Run. The Next.js application will be containerized with a multi-stage Dockerfile that builds the application and sets up a production Node.js server.

**Network - **Configuration:**** The Cloud Run service will be fronted by a Global External HTTPS Load Balancer. This provides a single global Anycast IP address, manages our SSL certificates via Google-Managed SSL Certificates, and allows us to enable Cloud CDN on the backend service to cache static assets (_next/static/*) at Google's edge locations for optimal performance.

#### Simple Explanation

We will host our marketing website on GCP Cloud Run. It's like a flexible, pay-as-you-go web server that's perfect for modern Next.js sites. It's fast because it can use Google's global network to serve content from a location near the visitor, and it's cheap because we don't pay anything if nobody is visiting the site.

3.2. The Tenant Onboarding User Flow (The Forms)
#### Technical Explanation

- **Create Account Page (/signup):** The user submits a form containing full_name, email, password, and company_name. On submission, the frontend makes a POST request to /api/auth/register. On success, a JWT is returned and stored in the client's local storage, and the user is programmatically redirected.

- **Select Plan & Enter Payment Page (/subscribe):** The user selects from a list of subscription plans. The frontend initializes the Stripe.js library and mounts a Stripe Elements form for payment details. On submission, the frontend sends the chosen plan_id (e.g., price_1L2M3N...) and the payment_method_id generated by Stripe to /api/billing/create-subscription.

- **Connect Data Source Page (/connect):** This page uses React state to conditionally render form fields. The user first selects agent_type from a dropdown. This selection then populates the data_source_type dropdown (e.g., if agent_type is "sales_agent," data_source_type shows "shopify"). This, in turn, renders the required text inputs (shop_url, access_token). On final submission, the frontend gathers all data into a single JSON object and sends it to /api/provision/start.

- **Provisioning In Progress Page (/dashboard/pending):** This page provides immediate feedback. It displays a status message and animated spinner. The frontend polls a /api/provision/status/{tenant_id} endpoint every 15 seconds. This endpoint checks the state of the provisioning process in our database. Once the status changes to "completed," the frontend redirects to /dashboard/main.

#### Simple Explanation

The process is a simple, four-step journey.

Create Account: You give us your name, email, and password.

Choose Plan: You pick a subscription plan and enter your payment details into a secure Stripe form.

Connect Your Data: You tell us what kind of AI agent you want and where your data is (e.g., your Shopify store's URL and an API key).

Wait for Setup: After you click "Finish," you'll see a page that says, "We're building your instance now!" We'll send you an email the moment it's ready.

### 3.3. The Onboarding Backend (The API)
#### Technical Explanation

These are FastAPI endpoints in our main NLyzer application, protected by JWT authentication where necessary. Pydantic models will be used for strict request validation.

#### POST /api/auth/register:

Payload (UserCreate model): full_name: str, email: EmailStr, password: str, company_name: str.

Action: Validates the payload, hashes the password using passlib, creates a new user and a corresponding tenant record in our central PostgreSQL database, generates a JWT containing user_id and tenant_id, and returns it.

#### POST /api/billing/create-subscription:

Payload (SubscriptionCreate model): plan_id: str, payment_method_id: str.

Action: Uses the Stripe Python library to find or create a Stripe Customer associated with the user_id. It attaches the payment_method_id to the customer and creates a new Stripe Subscription with the specified plan_id. It updates the tenant's record in our database with their stripe_customer_id and sets subscription_status to "active".

#### POST /api/provision/start:

Payload (ProvisioningRequest model): agent_type: str, data_source_type: str, config_details: Dict[str, Any], credentials: Dict[str, str].

Action: This is the key handshake endpoint. It retrieves the tenant_id from the authenticated JWT, constructs a JSON message that matches the format expected by our Provisioning Cloud Function, and publishes this message to the provisioning-requests GCP Pub/Sub topic. It logs the publish action and immediately returns a 202 Accepted HTTP status code to the frontend, indicating the request has been successfully queued for asynchronous processing.

#### Simple Explanation

Our website's backend has three main APIs.

Create User API: This takes your sign-up details and creates your account.

Handle Payment API: This securely communicates with Stripe to set up your subscription plan.

Start Building API: This takes all your setup info, wraps it into a digital work order, and drops that order into a special mailbox (GCP Pub/Sub). Our provisioning robot checks this mailbox and starts building your instance.

## 4. The Universal Data Ingestion Strategy
#### Technical Explanation

**Foundational Features (from repository analysis):**
The core of this system is a factory pattern implemented in nlweb/data_loaders/__init__.py. The get_data_loader function in this file dynamically imports and instantiates the correct loader class based on the type key provided in the YAML configuration. My analysis of the nlweb/data_loaders/ directory confirms the following built-in loaders:

- **shopify:** Implemented in shopify_loader.py. Instantiates ShopifyLoader, which uses the Shopify Admin API to ingest product, collection, and page data. Requires a config block with shop_url and access_token.

- **sitemap:** Implemented in sitemap_loader.py. Instantiates SitemapLoader, which fetches and parses a sitemap.xml file, then crawls the listed URLs. Requires a config block with sitemap_url.

- **website:** Implemented in website_loader.py. Instantiates WebsiteLoader, which performs a basic recursive crawl of a website starting from a given base_url.

Proposed Solution (for unsupported platforms):
The repository does not contain pre-built loaders for WooCommerce, BigCommerce, or Magento. To support these platforms, our engineering team will create new Python modules (e.g., woocommerce_loader.py) within the nlweb/data_loaders/ directory. Each new module will define a class that inherits from a common base class, implements a load() method to handle the platform-specific API interactions, and is registered in the get_data_loader factory function.

#### Simple Explanation

We ingest Shopify data using the built-in Shopify data loader. We ingest data from any standard website using the Sitemap and Website crawlers. We configure these using a simple YAML instruction file for each client. For other platforms like WooCommerce, we will build new, custom loaders that plug into the existing system.

## 5. The Action & Tool-Using Agent Strategy (MCP Integration)
#### Technical Explanation

**Foundational Features (from repository analysis):**
A factory in nlweb/tools/__init__.py dynamically loads tool-handling classes based on the tools configuration block in nlweb_config.yml. The LLM is then prompted to use these tools by name.

a. Website Actions (website_action_tool): This tool enables the agent to trigger actions in the client-side NLyzer Widget. The NLWeb backend sends a JSON payload to the frontend for execution.

Configuration (nlweb_config.yml):

```yaml
tools:
  - type: website_action_tool
    config:
      actions:
        - name: "add_to_cart"
          description: "Adds a specific product to the user's shopping cart. Use when the user explicitly asks to add an item."
          js_function: "Nlyzer.addToCart(productId, quantity);"
```

b. External Tools (api_tool): This tool allows the NLWeb backend to make server-side API calls to third-party services.

Configuration (nlweb_config.yml):

```yaml
tools:
  - type: api_tool
    config:
      name: "weather_api_tool"
      description: "Gets the current weather for a given city."
      api_url: "https://api.weather.com/v1/current?q={city}"
      api_key: "projects/nlyzer-ops/secrets/weather-api-key/versions/latest"
```

The APITool class in nlweb/tools/api_tool.py is responsible for making the authenticated HTTP request.

c. Multimodality (Visual Search):

Entry Point: The FastAPI server in nlweb/main.py will define an endpoint POST /v1/visual_search that accepts multipart/form-data.

Mechanism: The request handler passes the image data to a nlweb/vision/processor.py module, which uses a model like CLIP to generate a vector embedding for a similarity search in Weaviate.

#### Simple Explanation

We can give NLWeb special abilities using tools. To add an item to a cart, we tell NLWeb what "add to cart" means, and it sends a command to our frontend widget to execute the action. To connect to a weather API, we give NLWeb the API address and a key, and it can fetch data on its own. For visual search, we have a special API endpoint where our widget can upload an image, which NLWeb analyzes and uses to find matching products.

## 6. The Agent Specialization Strategy
#### Technical Explanation

We will create distinct "agent types" for different industries by providing a unique, curated nlweb_config.yml for each tenant based on their selection during onboarding.

- **E-commerce "Sales Agent":** The nlweb_config.yml for this type will include a data_loaders entry for shopify and a tools entry for website_action_tool with add_to_cart and save_for_later actions.

- **Travel "Booking Agent":** This configuration will feature a custom api data loader for a travel Global Distribution System (GDS), an api_tool for weather checks, and a website_action_tool to pre-fill booking forms.

- **"Documentation Agent" for a SaaS company:** This configuration will be minimalist, containing only a sitemap data loader pointing to the client's documentation site and an empty tools array.

#### Simple Explanation

We create specialized agents by giving them different instruction files. A Sales Agent gets an instruction file that connects to Shopify and knows how to "add to cart." A Travel Agent connects to booking systems and weather APIs. A Documentation Agent only reads help pages and has no other tools.

## 7. The Data Intelligence & Analytics Strategy

### 7.1. The BI Data Pipeline Foundation
#### Technical Explanation

- **Structured Logging:** Both the NLWeb backend and the frontend NLyzer Widget will be instrumented to log key events as structured JSON objects to stdout.

- **Log Ingestion:** GCP Cloud Logging automatically captures all stdout streams from every tenant's Cloud Run instance.

- **Data Routing:** A Log Sink is configured in Cloud Logging to filter for our specific JSON logs (e.g., jsonPayload.event IS NOT NULL). It forwards these logs to a central Google Pub/Sub topic in our main operations project.

- **Data - **Pipeline:**** A Dataflow job (Streaming) subscribes to the Pub/Sub topic. It performs validation, schema enforcement, and minor transformations before streaming the data into our central BigQuery data warehouse. The data will be stored in a single table, partitioned by timestamp and clustered by tenant_id.

#### Simple Explanation

Our data strategy is our secret sauce. First, we set up a pipeline: every important user click becomes a structured log message. These logs are automatically collected by GCP, filtered, and sent to BigQuery, our master analytics database.

### 7.2. The Expanded Event Schema
#### Technical Explanation

Each event includes tenant_id, session_id, user_id, and timestamp.

- **session_start:** Triggered by the widget on load. Payload: { "device_type", "browser", "initial_url" }.

- **query_received:** Triggered by the backend. Payload: { "user_query", "query_type": "text|visual" }.

- **query_refinement:** Triggered by the widget on filter/sort. Payload: { "refinement_type", "refinement_key", "refinement_value" }.

- **product_view:** Triggered by the widget on product click. Payload: { "product_id", "source_query", "result_rank" }.

- **tool_executed:** Triggered by the backend when an action is taken. Payload: { "tool_name", "action_name", "parameters" }.

- **null_search_result:** Triggered by the backend on zero results. Payload: { "query" }.

- **feedback_provided:** Triggered by the widget on feedback click. Payload: { "rating": "positive|negative", "source_query", "llm_response" }.

#### Simple Explanation

We log every important customer action as a unique event. We log when a customer starts a session, when they refine a search, when they view a product, and when they add to cart. We also make a special note of any unanswered questions.

### 7.3. Advanced KPIs and Actionable Insights
#### Technical Explanation

- **Search Funnel Drop-off Analysis:** A funnel chart visualizing the percentage drop-off between query_received -> product_view -> tool_executed events.

- **Content Gap Analysis:** A table of the top queries from null_search_result events.

- **Highest Converting Search Paths:** A pathing analysis query in BigQuery to identify the most frequent sequences of query_received and query_refinement events that lead to a tool_executed event within the same session.

- **Most Effective Refinements:** A table showing the refinement_key and refinement_value pairs with the highest correlation to conversion events.

- **AI Interaction Quality Score:** A gauge chart showing (positive_ratings / total_ratings) * 100.

#### Simple Explanation

We will build powerful new dashboard widgets. One will show a funnel illustrating where customers drop off. Another will be a list of "Top Unanswered Questions." A third will reveal the "Golden Paths"—the exact sequence of searches and filters that lead to the most sales.

### 7.4. The 'Data Analyst Chat Box' Architecture
#### Technical Explanation

**The Authorized View Model:** During provisioning, our Cloud Function will execute a DDL query to create a tenant-specific, authorized BigQuery view.

Example DDL command for tenant 'acme-corp-456':

```sql
CREATE VIEW `nlyzer-ops-project.tenant_views.vw_acme_corp_456` AS
SELECT *
FROM `nlyzer-ops-project.analytics.events`
WHERE tenant_id = 'acme-corp-456';
```

**IAM Enforcement:** The service account used by our "Data Analyst Chat Box" API (sa-analytics-agent@...) will have NO permissions on the underlying analytics.events table. Instead, it will be granted the roles/bigquery.dataViewer permission only on the specific tenant's view.

**Agent Invocation:** The backend invokes the LLM with a prompt like: "You are a helpful data analyst. You can query the BigQuery view named vw_acme_corp_456 to answer questions."

**Secure Execution:** The LLM generates a SQL query against the view. Because the agent's identity physically cannot see any other view or the master table, it is impossible for it to leak data, even if the generated SQL were faulty.

#### Simple Explanation

To prevent our Data Analyst Chat Box from ever mixing up client data, we build them a private, sealed library room (an Authorized View) that only contains their books. We then give our Data Analyst AI a key that only opens that specific room. It's now physically impossible for the AI to access the wrong client's data.

## 8. The Frontend Component Architecture
#### Technical Explanation

**Tech Stack:** Next.js (with React).

**Componentization Plan (Atomic Design):** The src/components/ directory will be structured into:

- **atoms/:** Button.tsx, Input.tsx, Spinner.tsx, Badge.tsx, Icon.tsx.

- **molecules/:** SearchBar.tsx, ProductCard.tsx, RangeSlider.tsx, ImageUploader.tsx.

- **organisms/:** ProductGrid.tsx, FilterSidebar.tsx, ProductDetailModal.tsx, ChatInterface.tsx.

**State Management Strategy:** Zustand. A central store (src/store/widgetStore.ts) will manage global widget state like isWidgetOpen, chatHistory, searchResults, and isLoading, while component-local state will use React's useState.

#### Simple Explanation

We will build our customer-facing NLyzer Widget using Next.js and React. We will organize our code using Atomic Design, starting with small "atoms" like buttons, combining them into "molecules" like a search bar, and assembling those into "organisms" like a complete product grid. To manage the widget's memory, we will use Zustand, a lightweight tool that acts as the widget's central brain.

## 9. The Operational & Security Hardening Plan

### 9.1. Observability & Monitoring Strategy
#### Technical Explanation

- **Core Services:** Google Cloud Monitoring and Cloud Logging.

- **Dashboards:** Each tenant's GCP Project will have a pre-configured Cloud Monitoring Dashboard visualizing key per-resource metrics.

- **Metrics to Track:** run.googleapis.com/request_latencies (p95, p99), run.googleapis.com/container/cpu/utilization, logging.googleapis.com/log_entry_count (filtered for severity=ERROR), compute.googleapis.com/instance/cpu/utilization, and compute.googleapis.com/instance/disk/used_bytes.

- **Alerting:** Cloud Monitoring Alerting Policies will be configured in a central operations project to monitor all tenant projects for thresholds (e.g., p99 latency > 2s, CPU > 80% for 15 mins, Disk > 90%) and route alerts to PagerDuty.

#### Simple Explanation

We will install security cameras and alarm systems for every client's server and database. We'll have a central security room (Google Cloud Monitoring) with a dedicated TV screen (Dashboard) for each client. If a server is running too slow or its hard drive is getting full, an alarm bell (Cloud Alerting) will automatically ring in our SRE team's office.

### 9.2. Database Management Strategy
#### Technical Explanation

- **Schema Migrations:** We will version the Weaviate schema. Idempotent Python migration scripts will be written for any change and run via a centrally managed job during maintenance windows.

- **Backup and Disaster Recovery (DR):** We will use GCP Persistent Disk Snapshots with a Resource Policy to automate daily snapshots (retained for 7 days) and weekly snapshots (retained for 4 weeks). The DR plan involves provisioning a new GCE instance from the latest stable snapshot and updating the Cloud Run service's WEAVIATE_URL environment variable.

#### Simple Explanation

For our databases, we have a clear plan. For updates, we have a special tool that carefully applies required changes. For safety, we take an automatic photocopy (Snapshot) of every client's database every single night. If a database ever breaks, we can fire up a new one from last night's copy in minutes.

### 9.3. CI/CD & Safe Deployment Strategy
#### Technical Explanation

- **Pipeline:** A GitHub Actions workflow (.github/workflows/deploy.yml) will define multiple, independent jobs. Each job will be responsible for a specific component (e.g., the API, the NLWeb image) and will only run if files in its designated path have been modified.

Path-Based Trigger Logic (deploy.yml example):

```yaml
name: NLyzer CI/CD Pipeline
on:
  push:
    branches: [ main ]
    paths:
      - 'nlyzer_api/**'
      - 'nlweb/**'
      - 'nlyzer_website/**'
jobs:
  deploy-api:
    if: "contains(toJSON(github.event.commits), 'nlyzer_api/')"
    # ...
  deploy-nlweb-image:
    if: "contains(toJSON(github.event.commits), 'nlweb/')"
    # ...
```

- **Progressive Delivery:** The deploy-nlweb-image job builds and pushes the new version-tagged image. The actual rollout to tenants remains a separate, manually-triggered workflow that allows an SRE to select the image tag to deploy, preserving the safety of the Canary/Bake/Promote process.

#### Simple Explanation

Our software assembly line (CI/CD pipeline) is now much smarter. If a developer only changes the website code, only the website crew is activated. The API and NLWeb engine crews don't get called. This path-based system saves time, reduces risk, and lets us deliver updates much more efficiently.

### 9.4. Cost Management & Resource Guardrails
#### Technical Explanation

- **Cost Controls:** Our Provisioning Function will create a GCP Budget with alert thresholds (50%, 90%, 100%) for each new tenant project.

- **Rate Limiting (Proposed Code Change):** We will implement application-level rate limiting on expensive LLM calls within the NLWeb backend. A tenant_id-based in-memory store will track request counts against plan limits. If a tenant exceeds their quota, the API will return an HTTP 429 Too Many Requests error.

#### Simple Explanation

To control costs, we put a spending limit on the credit card for each client's project. We set an alarm to go off if the spending gets too high. Most importantly, since the AI's "thinking" is expensive, we build a fuse box into our NLWeb software. Each client gets a certain number of AI requests per day based on their plan. If they exceed that limit, the fuse for that service blows.

### 9.5. Network & Infrastructure Security
#### Technical Explanation

- **Network Design:** A Shared VPC model where the NLyzer operations project is the "host" and tenant projects are "service projects."

- **Tenant Isolation:** VPC Firewall Rules will be used with network tags. A db-{tenant_id} tag on the GCE instance and a run-{tenant_id} tag on the Cloud Run service will be used to create an ingress rule that allows traffic on the database port only if the source and destination tags match. A default-deny egress rule will prevent databases from initiating outbound connections.

- **External Threat Protection:** A Global External HTTPS Load Balancer will route all traffic. A Google Cloud Armor security policy will be attached to it with pre-configured WAF rules to mitigate the OWASP Top 10 and provide DDoS protection.

#### Simple Explanation

We build our entire service inside a secure digital fortress. Each client gets their own private, high-walled room (firewall rules) inside. The rules state that the server in a room can only talk to the database in that same room. All visitor traffic must pass through a heavily guarded main gate (Load Balancer with Cloud Armor), where security guards check for any known threats.

## 10. Development & Contribution Policies

### 10.1. Upstream Maintenance for NLWeb Fork
#### Technical Explanation

1. Git Remote - **Configuration:**
Every developer working on our core NLWeb extension must configure their local repository with an upstream remote that points to the official open-source project.

```bash
git remote add upstream https://github.com/nlweb-ai/NLWeb.git
git remote -v
```

2. Update Cadence & Process:
On the first Monday of each quarter, the designated Lead Engineer will perform the upstream sync.

```bash
git checkout main
git pull origin main
git fetch upstream
git merge upstream/main --no-ff
```

3. Conflict Resolution & Testing:

Merge conflicts will be resolved locally, prioritizing upstream changes unless they directly conflict with our proprietary extensions.

After resolving conflicts, the code must be pushed to a feature branch (e.g., feature/upstream-sync-q3-2025), not directly to main.

A pull request from this branch will trigger our full CI/CD pipeline, including all tests. The PR requires review and approval before being merged.

#### Simple Explanation

Our NLyzer engine is built using an open-source engine block from another company. To make sure we always have their latest safety features and performance improvements, we have a formal maintenance schedule.

- **Configuration:** We've programmed our mechanics' tools to know the address of the original engine factory.

- **Schedule:** Every three months, our lead mechanic connects to the factory to download their latest blueprints and parts.

- **Safe Installation:** They carefully merge these new parts with our own custom modifications on a test engine. This test engine goes through rigorous quality checks. Only after it passes every single test do we approve the changes and update the engines used in our production service.
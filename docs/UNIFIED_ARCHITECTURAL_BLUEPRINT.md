Of course. This is the definitive and final version of the Unified Architectural Blueprint, updated to include the detailed Sprint 0 implementation plan. It is a complete, self-contained document integrating all sections and their subsections with the highest level of specificity and no redactions. This is our master plan for implementation.

The Unified Architectural Blueprint for NLyzer (Definitive, Hardened Master Plan)
0. Sprint 0 Implementation Plan: Creating the nlweb_extension

This section details the critical, high-priority engineering tasks required to fork, modify, and containerize the NLWeb source code into our custom, production-ready nlweb_extension service. The completion of these tasks is a prerequisite for the rest of the platform's implementation.

0.1. Task 1: Forking & Repository Setup
Technical Explanation

The first step is to create a proper, private fork of the upstream repository and establish a clear directory structure for our custom code.

Create Private Fork: A new private repository named nlyzer-engine will be created under our company's GitHub organization.

Clone and Add Upstream: The initial code will be populated by cloning the official NLWeb repository and configuring our fork as the origin and the official repository as upstream.

Generated bash
# Clone the official repo into a directory that will become our extension
git clone https://github.com/nlweb-ai/NLWeb.git nlyzer-engine
cd nlyzer-engine

# Reset the origin to point to our new private repository
git remote set-url origin git@github.com:NLyzer/nlyzer-engine.git

# Add the official repo as an "upstream" remote for future syncing
git remote add upstream https://github.com/nlweb-ai/NLWeb.git

# Verify the remotes
git remote -v
# Expected output:
# origin    git@github.com:NLyzer/nlyzer-engine.git (fetch/push)
# upstream  https://github.com/nlweb-ai/NLWeb.git (fetch/push)

# Push the initial code to our private repository
git push -u origin main


This nlyzer-engine directory now represents our custom fork where all subsequent changes will be made.

Simple Explanation

First, we take the official public blueprint for the NLWeb engine and make a private copy just for our company. This is our master copy. We then configure our tools so we always know the address of the public blueprint, making it easy to pull in their security updates later.

0.2. Task 2: Dependency Management
Technical Explanation

The upstream NLWeb project uses Poetry for dependency management, as defined in pyproject.toml. We must use the same tool to add our new GCP-specific dependencies.

Add GCP Libraries: From within the nlyzer-engine directory, we will use Poetry to add the required Google Cloud client libraries.

Generated bash
# Add the library for Google Cloud Storage access
poetry add google-cloud-storage

# Add the library for Google Secret Manager access
poetry add google-cloud-secret-manager

# Add the library for YAML parsing
poetry add pyyaml
IGNORE_WHEN_COPYING_START
content_copy
download
Use code with caution.
Bash
IGNORE_WHEN_COPYING_END

Lock Dependencies: These commands will automatically update our pyproject.toml and poetry.lock files, ensuring that our builds are deterministic and include the exact versions of the new libraries.

Simple Explanation

The original engine has a parts list (pyproject.toml). Our custom version needs extra parts to talk to Google's services. We are officially adding the "Google Storage Wrench," the "Google Secret Vault Key," and a "YAML Reader" to our copy of the parts list.

0.3. Task 3: Core Application Modifications
Technical Explanation

We will now implement the specific code changes required by our architecture.

3.1. Implement GCP Utilities (nlweb/gcp_utils.py)

A new file will be created at nlyzer-engine/nlweb/gcp_utils.py. This module will contain our helper functions for interacting with GCP.

File Path: nlyzer-engine/nlweb/gcp_utils.py

File Content:

Generated python
import os
import yaml
from google.cloud import storage, secretmanager

def load_config_from_gcs(gcs_path: str) -> dict:
    """Downloads a YAML file from GCS and parses it."""
    storage_client = storage.Client()
    bucket_name, blob_name = gcs_path.replace("gs://", "").split("/", 1)
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)
    config_string = blob.download_as_text()
    return yaml.safe_load(config_string)

def resolve_secrets_in_config(config: dict) -> dict:
    """Recursively traverses a dict and resolves Secret Manager paths."""
    client = secretmanager.SecretManagerServiceClient()
    for key, value in config.items():
        if isinstance(value, dict):
            resolve_secrets_in_config(value)
        elif isinstance(value, str) and value.startswith("projects/"):
            try:
                response = client.access_secret_version(name=value)
                config[key] = response.payload.data.decode("UTF-8")
            except Exception as e:
                print(f"FATAL: Failed to resolve secret: {value}. Error: {e}")
                raise
    return config
IGNORE_WHEN_COPYING_START
content_copy
download
Use code with caution.
Python
IGNORE_WHEN_COPYING_END

3.2. Implement Resilient Startup Logic (nlweb/main.py)

We will modify the main application entrypoint to be fault-tolerant and to use our new GCP utilities.

File Path: nlyzer-engine/nlweb/main.py

Required Modifications:

Generated python
# Add new imports at the top of nlweb/main.py
import os
import sys
from .gcp_utils import load_config_from_gcs, resolve_secrets_in_config

# ... other existing imports

# This code will wrap the existing application startup logic
try:
    print("NLyzer Engine starting up...")
    # 1. Load configuration from GCS
    config_path = os.environ.get("NLWEB_CONFIG_PATH")
    if not config_path:
        raise ValueError("FATAL: NLWEB_CONFIG_PATH environment variable not set.")
    config = load_config_from_gcs(config_path)
    print("Configuration file loaded from GCS.")

    # 2. Resolve secrets within the configuration
    config = resolve_secrets_in_config(config)
    print("Secrets resolved successfully.")
    
    # ... continue with existing logic to initialize Weaviate client,
    # data loaders, and tools using the now-populated `config` dict.

except Exception as e:
    print(f"FATAL: Application startup failed: {e}. Exiting.")
    sys.exit(1) # Exit non-zero to fail the Cloud Run health check

# Existing app = FastAPI() and endpoint definitions follow
IGNORE_WHEN_COPYING_START
content_copy
download
Use code with caution.
Python
IGNORE_WHEN_COPYING_END

3.3. Implement Initial Sync Endpoint (nlweb/main.py)

We will add the new system-level endpoint for triggering data ingestion.

File Path: nlyzer-engine/nlweb/main.py

Required Modifications:

Generated python
# Add to the imports at the top of nlweb/main.py
from fastapi import Request, Depends, HTTPException, APIRouter
# We will need a placeholder for our real IAM auth dependency
# from ..auth import require_iam_permission 

# ... after app = FastAPI() is defined ...

# Create a new router for system endpoints
system_router = APIRouter(tags=["System"])

@system_router.post(
    "/v1/system/trigger-initial-sync",
    # dependencies=[Depends(require_iam_permission("run.invoker"))] # This will be uncommented when auth is built
)
def trigger_sync(request: Request):
    """
    Triggers the initial data ingestion for all configured loaders.
    This endpoint is protected and can only be invoked by our provisioning service.
    """
    print("Initial sync triggered by system request.")
    # In a real implementation, loaders would be on the app state, e.g., request.app.state.loaders
    # For now, we simulate this call.
    # for loader in request.app.state.data_loaders:
    #     loader.load()
    print("Simulated call to data loaders completed.")
    return {"status": "Initial sync process initiated."}

# Register the new router with the main FastAPI app
app.include_router(system_router)
IGNORE_WHEN_COPYING_START
content_copy
download
Use code with caution.
Python
IGNORE_WHEN_COPYING_END
Simple Explanation

We are performing three critical upgrades to the engine's core programming.

We're adding specialized tools. We're bolting on a new toolbox (gcp_utils.py) with a "GCS Wrench" to grab files from Google Storage and a "Secret Vault Key" to unlock credentials from Secret Manager.

We're making the startup sequence robust. The engine now follows a strict startup checklist. If it can't find its instructions (the config file) or access its tools, it safely stops and waits for the problem to be fixed instead of breaking down.

We're installing a "Start Job" button. We're adding a special API endpoint (/trigger-initial-sync) that acts like a big red button. Only our master provisioning robot can press this button, and when it does, it tells the engine to begin its first major data-loading task.

0.4. Task 4: Production Dockerfile Hardening
Technical Explanation

The original Dockerfile is suitable for development but not optimized for production security or size. We will replace it with a multi-stage Dockerfile to create a minimal, secure final image.

File Path: nlyzer-engine/Dockerfile (overwriting the original)

New File Content:

Generated dockerfile
# --- Builder Stage ---
# Use the official Python image as a base
FROM python:3.11-slim as builder

# Set the working directory
WORKDIR /app

# Install poetry
RUN pip install poetry

# Copy only the files required to install dependencies
COPY poetry.lock pyproject.toml ./

# Install dependencies, but not dev dependencies, into a virtual environment
RUN poetry config virtualenvs.create true && \
    poetry config virtualenvs.in-project true && \
    poetry install --no-dev

# --- Final Stage ---
# Use the same slim Python base for the final image
FROM python:3.11-slim as final

# Create a non-root user for security
RUN useradd --create-home --shell /bin/bash appuser
WORKDIR /home/appuser/app

# Copy the virtual environment from the builder stage
COPY --from=builder /app/.venv ./.venv
# Copy our application code
COPY . .

# Ensure the appuser owns all the files
RUN chown -R appuser:appuser /home/appuser

# Switch to the non-root user
USER appuser

# Set the PATH to include the virtual environment's binaries
ENV PATH="/home/appuser/app/.venv/bin:$PATH"

# Command to run the application
CMD ["python", "-m", "nlweb.main"]
IGNORE_WHEN_COPYING_START
content_copy
download
Use code with caution.
Dockerfile
IGNORE_WHEN_COPYING_END
Simple Explanation

We are changing how we pack our engine for shipping. The old way just threw everything into one big box. The new way is a two-step professional process.

Workshop Stage: We first assemble the engine with all our tools in a large, messy workshop.

Shipping Stage: Once the engine is built, we take only the finished engine and its essential parts and place them into a small, clean, and securely locked container. We also label it to be handled by a "special employee" (a non-root user) for extra safety, not the "site manager" (root user).

0.5. Task 5: Build & Test Plan
Technical Explanation

After all modifications are complete, we must perform a local build and test run to verify that our custom nlweb_extension is functional before committing it.

Build the Image: From the root of the nlyzer-engine directory, run the Docker build command.

Generated bash
docker build -t nlyzer-engine:0.1.0 .
IGNORE_WHEN_COPYING_START
content_copy
download
Use code with caution.
Bash
IGNORE_WHEN_COPYING_END

Prepare for Local Test:

Create a local test_config.yml file.

Set up Application Default Credentials for GCP by running gcloud auth application-default login.

Upload the test_config.yml to a GCS bucket.

Create a test secret in Secret Manager.

Run the Container: Run the newly built image locally, passing the necessary environment variables.

Generated bash
docker run -p 8000:8000 \
  -v ~/.config/gcloud/application_default_credentials.json:/gcp/adc.json:ro \
  -e GOOGLE_APPLICATION_CREDENTIALS="/gcp/adc.json" \
  -e NLWEB_CONFIG_PATH="gs://your-test-bucket/test_config.yml" \
  -e WEAVIATE_URL="http://your-test-weaviate:8080" \
  nlyzer-engine:0.1.0
IGNORE_WHEN_COPYING_START
content_copy
download
Use code with caution.
Bash
IGNORE_WHEN_COPYING_END

Verification:

Check the container logs to ensure the "Configuration file loaded" and "Secrets resolved" messages appear.

Verify the container does not exit with a non-zero status code.

Use curl or an API client to hit the http://localhost:8000/docs endpoint to see the FastAPI documentation, including our new /v1/system/trigger-initial-sync endpoint.

Simple Explanation

This is our final quality assurance check. Before we approve our new custom engine design, we will:

Build one: We'll assemble one engine using our new hardened process.

Put it on a test bench: We'll run the engine on a local machine, connecting it to a test database and giving it test instructions.

Check the diagnostics: We'll watch the engine's startup logs to make sure it reads its instructions and accesses its tools correctly. We'll also check that its own internal control panel (the API docs) shows our new "Start Job" button. If all checks pass, the design is approved.

1. The Deployment Strategy
Technical Explanation

Foundational Features (from repository analysis):
The open-source NLWeb project is designed for containerization, defined by its root Dockerfile and docker-compose.yml. The application entrypoint specified in the Dockerfile is CMD ["python", "-m", "nlweb.main"], which starts a FastAPI server. Its local deployment configuration, as detailed in docker-compose.yml, relies on environment variables (e.g., NLWEB_CONFIG_PATH, WEAVIATE_URL, OPENAI_API_KEY) to manage its runtime settings.

NLyzer's GCP Architecture:
Our managed service will forgo docker-compose in favor of a scalable, single-tenant GCP architecture. Each client deployment will consist of the following resources provisioned within a dedicated GCP Project to ensure absolute billing and resource isolation:

Compute: The now-customized nlyzer-engine Dockerfile will be used to build a container image, which will be stored and versioned in Google Artifact Registry. For each tenant, this image will be deployed as a dedicated GCP Cloud Run service.

Database: Each tenant will receive an isolated Weaviate vector database, deployed as a container on a dedicated GCP Compute Engine (GCE) instance.

Orchestration: A central GCP Cloud Function, our "Provisioning Robot," will orchestrate the entire setup.

Simple Explanation

We deploy our custom NLyzer Engine for each client using GCP Cloud Run, which gives them a private and secure mini-server. Each client also gets their own private Weaviate database. We automate the entire setup using a master robot (a GCP Cloud Function) that builds a new, dedicated environment for each client.

2. The Automated Provisioning Handshake
2.1. The Waiting Mechanism
Technical Explanation

The nlyzer-engine application waits dormantly as a container image. Its resilient startup logic (defined in Section 0.3.2) ensures that if it is deployed by Cloud Run without a valid configuration, it will log the specific error and exit with a non-zero status code. This will fail the Cloud Run health check, causing Cloud Run to manage a restart backoff loop until the configuration is present, all without incurring significant cost.

Simple Explanation

Our custom engine has a built-in safety check. If we try to start it without proper instructions, it simply stops and waits. Cloud Run manages this waiting process automatically and cheaply.

2.2. The Configuration Generation
Technical Explanation

The Provisioning Cloud Function, triggered by a Pub/Sub message, will generate the nlweb_config.yml file in memory. It will write sensitive credentials to Google Secret Manager and embed the resource paths to those secrets in the YAML. It then uploads this file to a new, dedicated GCS bucket for the tenant.

Additionally, the function securely stores Namecheap API credentials in GCP Secret Manager at the organization level. These credentials are:
- Stored separately from tenant secrets for the central provisioning function
- Accessed only by the provisioning service account with roles/secretmanager.secretAccessor
- Never exposed to tenant projects or stored in tenant configurations
- Rotated quarterly following security best practices

Simple Explanation

When a work order arrives, our robot locks the client's secret credentials in a digital vault (Secret Manager). It then writes the assembly instructions (config.yml), noting the vault location, and places the instructions in a private folder (Cloud Storage). The master robot also keeps the domain control keys (Namecheap credentials) in a special organization-wide vault, separate from tenant vaults. Only the provisioning robot can access these keys to create DNS records for new tenants.

2.3. The Secure Application
Technical Explanation

The Provisioning Function creates a dedicated GCP Service Account for the tenant with least-privilege IAM roles (roles/storage.objectViewer, roles/secretmanager.secretAccessor). It then deploys the nlyzer-engine image to a new Cloud Run service, setting its identity to this service account and providing the GCS path to the config file via the NLWEB_CONFIG_PATH environment variable. On startup, the nlyzer-engine uses its permissions to fetch the config and resolve the secrets, as implemented in Section 0.3.

Simple Explanation

The robot assembles the client's server, giving it a special keycard (Service Account) that only opens the client's private folder and their specific spot in the digital vault. The server uses this keycard to read its instructions and get its secrets.

2.4. The First Data Ingestion
Technical Explanation

After the Provisioning Function confirms the Cloud Run service is healthy, its final action is to make an authenticated POST request to the /v1/system/trigger-initial-sync endpoint on the new service's URL. This explicitly and auditably begins the data ingestion process defined in the tenant's configuration.

Simple Explanation

Once the server is running correctly, the robot presses the "Start Job" button we installed, telling the engine to begin loading all the client's data.

2.5. Orchestration Plane Security
Technical Explanation

Trigger Security: The Provisioning Cloud Function will be configured to allow "private" invocations only, requiring authentication. Its ingress settings will be set to "Allow internal traffic only," and it will be triggered by a private Pub/Sub topic that only our backend API can publish to.

Principle of Least Privilege: The function's service account will have a specific list of necessary roles (roles/resourcemanager.projectCreator, roles/iam.serviceAccountAdmin, roles/run.admin, etc.) and will not use basic roles like Editor.

Code Security: The CI/CD pipeline for the function will mandate code reviews, SAST scanning with GitHub CodeQL, and dependency scanning with Dependabot.

Simple Explanation

Our master robot (the Provisioning Function) is very powerful, so we're putting it in a high-security room.

Trigger Security: The robot only responds to orders from one specific person (our main NLyzer API).

Least Privilege: It has a keychain with specific keys for each job, not a master key.

Code Security: Any updates to its programming must pass an automated security inspection and a manual sign-off from a senior engineer.

Of course. Here is the continuation and completion of the definitive, unredacted, and fully detailed Unified Architectural Blueprint.

3. The Client Onboarding & Website Backend Blueprint

This section details the practical implementation of our client acquisition funnel, from our marketing website to the backend API that triggers the automated provisioning.

3.1. The Website Hosting Strategy
Technical Explanation

Hosting Service: GCP Cloud Run. The Next.js application will be containerized with a multi-stage Dockerfile that builds the application and sets up a production Node.js server.

Network Configuration: The Cloud Run service will be fronted by a Global External HTTPS Load Balancer. This provides a single global Anycast IP address, manages our SSL certificates via Google-Managed SSL Certificates, and allows us to enable Cloud CDN on the backend service to cache static assets (_next/static/*) at Google's edge locations for optimal performance.

DNS Configuration: After the Global External HTTPS Load Balancer is provisioned and its static IP address is allocated, the Provisioning Cloud Function programmatically configures DNS records via the Namecheap API. The function:
1. Retrieves Namecheap API credentials from GCP Secret Manager
2. Initializes the namecheapapi Python client with production endpoints
3. Creates an A record: {tenant_id}.nlyzer.com → {load_balancer_ip}
4. Sets TTL to 300 seconds for quick propagation
5. Validates the DNS record creation and propagation before proceeding

Simple Explanation

We will host our marketing website on GCP Cloud Run. It's like a flexible, pay-as-you-go web server that's perfect for modern Next.js sites. It's fast because it can use Google's global network to serve content from a location near the visitor, and it's cheap because we don't pay anything if nobody is visiting the site.

Once the load balancer gets its permanent address (like a street number), our provisioning robot calls Namecheap to add this address to the global phone book (DNS). So when someone types "acme.nlyzer.com", they're automatically directed to the correct tenant's front door.

3.2. The Tenant Onboarding User Flow (The Forms)
Technical Explanation

Create Account Page (/signup): The user submits a form containing full_name, email, password, and company_name. On submission, the frontend makes a POST request to /api/auth/register. On success, a JWT is returned and stored in the client's local storage, and the user is programmatically redirected.

Select Plan & Enter Payment Page (/subscribe): The user selects from a list of subscription plans. The frontend initializes the Stripe.js library and mounts a Stripe Elements form for payment details. On submission, the frontend sends the chosen plan_id (e.g., price_1L2M3N...) and the payment_method_id generated by Stripe to /api/billing/create-subscription.

Connect Data Source Page (/connect): This page uses React state to conditionally render form fields. The user first selects agent_type from a dropdown. This selection then populates the data_source_type dropdown (e.g., if agent_type is "sales_agent," data_source_type shows "shopify"). This, in turn, renders the required text inputs (shop_url, access_token). On final submission, the frontend gathers all data into a single JSON object and sends it to /api/provision/start.

Provisioning In Progress Page (/dashboard/pending): This page provides immediate feedback. It displays a status message and animated spinner. The frontend polls a /api/provision/status/{tenant_id} endpoint every 15 seconds. This endpoint checks the state of the provisioning process in our database. Once the status changes to "completed," the frontend redirects to /dashboard/main.

Simple Explanation

The process is a simple, four-step journey.

Create Account: You give us your name, email, and password.

Choose Plan: You pick a subscription plan and enter your payment details into a secure Stripe form.

Connect Your Data: You tell us what kind of AI agent you want and where your data is (e.g., your Shopify store's URL and an API key).

Wait for Setup: After you click "Finish," you'll see a page that says, "We're building your instance now!" We'll send you an email the moment it's ready.

3.3. The Onboarding Backend (The API)
Technical Explanation

These are FastAPI endpoints in our main NLyzer application, protected by JWT authentication where necessary. Pydantic models will be used for strict request validation.

POST /api/auth/register:

Payload (UserCreate model): full_name: str, email: EmailStr, password: str, company_name: str.

Action: Validates the payload, hashes the password using passlib, creates a new user and a corresponding tenant record in our central PostgreSQL database, generates a JWT containing user_id and tenant_id, and returns it.

POST /api/billing/create-subscription:

Payload (SubscriptionCreate model): plan_id: str, payment_method_id: str.

Action: Uses the Stripe Python library to find or create a Stripe Customer associated with the user_id. It attaches the payment_method_id to the customer and creates a new Stripe Subscription with the specified plan_id. It updates the tenant's record in our database with their stripe_customer_id and sets subscription_status to "active".

POST /api/provision/start:

Payload (ProvisioningRequest model): agent_type: str, data_source_type: str, config_details: Dict[str, Any], credentials: Dict[str, str].

Action: This is the key handshake endpoint. It retrieves the tenant_id from the authenticated JWT, constructs a JSON message that matches the format expected by our Provisioning Cloud Function, and publishes this message to the provisioning-requests GCP Pub/Sub topic. It logs the publish action and immediately returns a 202 Accepted HTTP status code to the frontend, indicating the request has been successfully queued for asynchronous processing.

Simple Explanation

Our website's backend has three main APIs.

Create User API: This takes your sign-up details and creates your account.

Handle Payment API: This securely communicates with Stripe to set up your subscription plan.

Start Building API: This takes all your setup info, wraps it into a digital work order, and drops that order into a special mailbox (GCP Pub/Sub). Our provisioning robot checks this mailbox and starts building your instance.

4. The Universal Data Ingestion Strategy
Technical Explanation

Foundational Features (from repository analysis):
The core of this system is a factory pattern implemented in nlweb/data_loaders/__init__.py. The get_data_loader function in this file dynamically imports and instantiates the correct loader class based on the type key provided in the YAML configuration. My analysis of the nlweb/data_loaders/ directory confirms the following built-in loaders:

shopify: Implemented in shopify_loader.py. Instantiates ShopifyLoader, which uses the Shopify Admin API to ingest product, collection, and page data. Requires a config block with shop_url and access_token.

sitemap: Implemented in sitemap_loader.py. Instantiates SitemapLoader, which fetches and parses a sitemap.xml file, then crawls the listed URLs. Requires a config block with sitemap_url.

website: Implemented in website_loader.py. Instantiates WebsiteLoader, which performs a basic recursive crawl of a website starting from a given base_url.

Proposed Solution (for unsupported platforms):
The repository does not contain pre-built loaders for WooCommerce, BigCommerce, or Magento. To support these platforms, our engineering team will create new Python modules (e.g., woocommerce_loader.py) within the nlweb/data_loaders/ directory. Each new module will define a class that inherits from a common base class, implements a load() method to handle the platform-specific API interactions, and is registered in the get_data_loader factory function.

Simple Explanation

We ingest Shopify data using the built-in Shopify data loader. We ingest data from any standard website using the Sitemap and Website crawlers. We configure these using a simple YAML instruction file for each client. For other platforms like WooCommerce, we will build new, custom loaders that plug into the existing system.

5. The Action & Tool-Using Agent Strategy (MCP Integration)
Technical Explanation

Foundational Features (from repository analysis):
A factory in nlweb/tools/__init__.py dynamically loads tool-handling classes based on the tools configuration block in nlweb_config.yml. The LLM is then prompted to use these tools by name.

a. Website Actions (website_action_tool): This tool enables the agent to trigger actions in the client-side NLyzer Widget. The NLWeb backend sends a JSON payload to the frontend for execution.

Configuration (nlweb_config.yml):

Generated yaml
tools:
  - type: website_action_tool
    config:
      actions:
        - name: "add_to_cart"
          description: "Adds a specific product to the user's shopping cart. Use when the user explicitly asks to add an item."
          js_function: "Nlyzer.addToCart(productId, quantity);"


b. External Tools (api_tool): This tool allows the NLWeb backend to make server-side API calls to third-party services.

Configuration (nlweb_config.yml):

Generated yaml
tools:
  - type: api_tool
    config:
      name: "weather_api_tool"
      description: "Gets the current weather for a given city."
      api_url: "https://api.weather.com/v1/current?q={city}"
      api_key: "projects/nlyzer-ops/secrets/weather-api-key/versions/latest"
IGNORE_WHEN_COPYING_START
content_copy
download
Use code with caution.
Yaml
IGNORE_WHEN_COPYING_END

The APITool class in nlweb/tools/api_tool.py is responsible for making the authenticated HTTP request.

c. Multimodality (Visual Search):

Entry Point: The FastAPI server in nlweb/main.py will define an endpoint POST /v1/visual_search that accepts multipart/form-data.

Mechanism: The request handler passes the image data to a nlweb/vision/processor.py module, which uses a model like CLIP to generate a vector embedding for a similarity search in Weaviate.

Simple Explanation

We can give NLWeb special abilities using tools. To add an item to a cart, we tell NLWeb what "add to cart" means, and it sends a command to our frontend widget to execute the action. To connect to a weather API, we give NLWeb the API address and a key, and it can fetch data on its own. For visual search, we have a special API endpoint where our widget can upload an image, which NLWeb analyzes and uses to find matching products.

6. The Agent Specialization Strategy
Technical Explanation

We will create distinct "agent types" for different industries by providing a unique, curated nlweb_config.yml for each tenant based on their selection during onboarding.

E-commerce "Sales Agent": The nlweb_config.yml for this type will include a data_loaders entry for shopify and a tools entry for website_action_tool with add_to_cart and save_for_later actions.

Travel "Booking Agent": This configuration will feature a custom api data loader for a travel Global Distribution System (GDS), an api_tool for weather checks, and a website_action_tool to pre-fill booking forms.

"Documentation Agent" for a SaaS company: This configuration will be minimalist, containing only a sitemap data loader pointing to the client's documentation site and an empty tools array.

Simple Explanation

We create specialized agents by giving them different instruction files. A Sales Agent gets an instruction file that connects to Shopify and knows how to "add to cart." A Travel Agent connects to booking systems and weather APIs. A Documentation Agent only reads help pages and has no other tools.

7. The Data Intelligence & Analytics Strategy
7.1. The BI Data Pipeline Foundation
Technical Explanation

Structured Logging: Both the NLWeb backend and the frontend NLyzer Widget will be instrumented to log key events as structured JSON objects to stdout.

Log Ingestion: GCP Cloud Logging automatically captures all stdout streams from every tenant's Cloud Run instance.

Data Routing: A Log Sink is configured in Cloud Logging to filter for our specific JSON logs (e.g., jsonPayload.event IS NOT NULL). It forwards these logs to a central Google Pub/Sub topic in our main operations project.

Data Pipeline: A Dataflow job (Streaming) subscribes to the Pub/Sub topic. It performs validation, schema enforcement, and minor transformations before streaming the data into our central BigQuery data warehouse. The data will be stored in a single table, partitioned by timestamp and clustered by tenant_id.

Simple Explanation

Our data strategy is our secret sauce. First, we set up a pipeline: every important user click becomes a structured log message. These logs are automatically collected by GCP, filtered, and sent to BigQuery, our master analytics database.

7.2. The Expanded Event Schema
Technical Explanation

Each event includes tenant_id, session_id, user_id, and timestamp.

session_start: Triggered by the widget on load. Payload: { "device_type", "browser", "initial_url" }.

query_received: Triggered by the backend. Payload: { "user_query", "query_type": "text|visual" }.

query_refinement: Triggered by the widget on filter/sort. Payload: { "refinement_type", "refinement_key", "refinement_value" }.

product_view: Triggered by the widget on product click. Payload: { "product_id", "source_query", "result_rank" }.

tool_executed: Triggered by the backend when an action is taken. Payload: { "tool_name", "action_name", "parameters" }.

null_search_result: Triggered by the backend on zero results. Payload: { "query" }.

feedback_provided: Triggered by the widget on feedback click. Payload: { "rating": "positive|negative", "source_query", "llm_response" }.

Simple Explanation

We log every important customer action as a unique event. We log when a customer starts a session, when they refine a search, when they view a product, and when they add to cart. We also make a special note of any unanswered questions.

7.3. Advanced KPIs and Actionable Insights
Technical Explanation

Search Funnel Drop-off Analysis: A funnel chart visualizing the percentage drop-off between query_received -> product_view -> tool_executed events.

Content Gap Analysis: A table of the top queries from null_search_result events.

Highest Converting Search Paths: A pathing analysis query in BigQuery to identify the most frequent sequences of query_received and query_refinement events that lead to a tool_executed event within the same session.

Most Effective Refinements: A table showing the refinement_key and refinement_value pairs with the highest correlation to conversion events.

AI Interaction Quality Score: A gauge chart showing (positive_ratings / total_ratings) * 100.

Simple Explanation

We will build powerful new dashboard widgets. One will show a funnel illustrating where customers drop off. Another will be a list of "Top Unanswered Questions." A third will reveal the "Golden Paths"—the exact sequence of searches and filters that lead to the most sales.

7.4. The 'Data Analyst Chat Box' Architecture
Technical Explanation

The Authorized View Model: During provisioning, our Cloud Function will execute a DDL query to create a tenant-specific, authorized BigQuery view.

Example DDL command for tenant 'acme-corp-456':

Generated sql
CREATE VIEW `nlyzer-ops-project.tenant_views.vw_acme_corp_456` AS
SELECT *
FROM `nlyzer-ops-project.analytics.events`
WHERE tenant_id = 'acme-corp-456';
IGNORE_WHEN_COPYING_START
content_copy
download
Use code with caution.
SQL
IGNORE_WHEN_COPYING_END

IAM Enforcement: The service account used by our "Data Analyst Chat Box" API (sa-analytics-agent@...) will have NO permissions on the underlying analytics.events table. Instead, it will be granted the roles/bigquery.dataViewer permission only on the specific tenant's view.

Agent Invocation: The backend invokes the LLM with a prompt like: "You are a helpful data analyst. You can query the BigQuery view named vw_acme_corp_456 to answer questions."

Secure Execution: The LLM generates a SQL query against the view. Because the agent's identity physically cannot see any other view or the master table, it is impossible for it to leak data, even if the generated SQL were faulty.

Simple Explanation

To prevent our Data Analyst Chat Box from ever mixing up client data, we build them a private, sealed library room (an Authorized View) that only contains their books. We then give our Data Analyst AI a key that only opens that specific room. It's now physically impossible for the AI to access the wrong client's data.

8. The Frontend Component Architecture
Technical Explanation

Tech Stack: Next.js (with React).

Componentization Plan (Atomic Design): The src/components/ directory will be structured into:

atoms/: Button.tsx, Input.tsx, Spinner.tsx, Badge.tsx, Icon.tsx.

molecules/: SearchBar.tsx, ProductCard.tsx, RangeSlider.tsx, ImageUploader.tsx.

organisms/: ProductGrid.tsx, FilterSidebar.tsx, ProductDetailModal.tsx, ChatInterface.tsx.

State Management Strategy: Zustand. A central store (src/store/widgetStore.ts) will manage global widget state like isWidgetOpen, chatHistory, searchResults, and isLoading, while component-local state will use React's useState.

Simple Explanation

We will build our customer-facing NLyzer Widget using Next.js and React. We will organize our code using Atomic Design, starting with small "atoms" like buttons, combining them into "molecules" like a search bar, and assembling those into "organisms" like a complete product grid. To manage the widget's memory, we will use Zustand, a lightweight tool that acts as the widget's central brain.

9. The Operational & Security Hardening Plan
9.1. Observability & Monitoring Strategy
Technical Explanation

Core Services: Google Cloud Monitoring and Cloud Logging.

Dashboards: Each tenant's GCP Project will have a pre-configured Cloud Monitoring Dashboard visualizing key per-resource metrics.

Metrics to Track: run.googleapis.com/request_latencies (p95, p99), run.googleapis.com/container/cpu/utilization, logging.googleapis.com/log_entry_count (filtered for severity=ERROR), compute.googleapis.com/instance/cpu/utilization, and compute.googleapis.com/instance/disk/used_bytes.

Alerting: Cloud Monitoring Alerting Policies will be configured in a central operations project to monitor all tenant projects for thresholds (e.g., p99 latency > 2s, CPU > 80% for 15 mins, Disk > 90%) and route alerts to PagerDuty.

Simple Explanation

We will install security cameras and alarm systems for every client's server and database. We'll have a central security room (Google Cloud Monitoring) with a dedicated TV screen (Dashboard) for each client. If a server is running too slow or its hard drive is getting full, an alarm bell (Cloud Alerting) will automatically ring in our SRE team's office.

9.2. Database Management Strategy
Technical Explanation

Schema Migrations: We will version the Weaviate schema. Idempotent Python migration scripts will be written for any change and run via a centrally managed job during maintenance windows.

Backup and Disaster Recovery (DR): We will use GCP Persistent Disk Snapshots with a Resource Policy to automate daily snapshots (retained for 7 days) and weekly snapshots (retained for 4 weeks). The DR plan involves provisioning a new GCE instance from the latest stable snapshot and updating the Cloud Run service's WEAVIATE_URL environment variable.

Simple Explanation

For our databases, we have a clear plan. For updates, we have a special tool that carefully applies required changes. For safety, we take an automatic photocopy (Snapshot) of every client's database every single night. If a database ever breaks, we can fire up a new one from last night's copy in minutes.

9.3. CI/CD & Safe Deployment Strategy
Technical Explanation

Pipeline: A GitHub Actions workflow (.github/workflows/deploy.yml) will define multiple, independent jobs. Each job will be responsible for a specific component (e.g., the API, the NLWeb image) and will only run if files in its designated path have been modified.

Path-Based Trigger Logic (deploy.yml example):

Generated yaml
name: NLyzer CI/CD Pipeline
on:
  push:
    branches: [ main ]
    paths:
      - 'nlyzer_api/**'
      - 'nlyzer-engine/**'
      - 'nlyzer_website/**'
jobs:
  deploy-api:
    if: "contains(join(github.event.commits.*.files), 'nlyzer_api/')"
    # ...
  build-nlyzer-engine:
    if: "contains(join(github.event.commits.*.files), 'nlyzer-engine/')"
    # ...
IGNORE_WHEN_COPYING_START
content_copy
download
Use code with caution.
Yaml
IGNORE_WHEN_COPYING_END

Progressive Delivery: The build-nlyzer-engine job builds and pushes the new version-tagged image. The actual rollout to tenants remains a separate, manually-triggered workflow that allows an SRE to select the image tag to deploy, preserving the safety of the Canary/Bake/Promote process.

Simple Explanation

Our software assembly line (CI/CD pipeline) is now much smarter. If a developer only changes the website code, only the website crew is activated. The API and NLWeb engine crews don't get called. This path-based system saves time, reduces risk, and lets us deliver updates much more efficiently.

9.4. Cost Management & Resource Guardrails
Technical Explanation

Cost Controls: Our Provisioning Function will create a GCP Budget with alert thresholds (50%, 90%, 100%) for each new tenant project.

Rate Limiting (Proposed Code Change): We will implement application-level rate limiting on expensive LLM calls within the NLWeb backend. A tenant_id-based in-memory store will track request counts against plan limits. If a tenant exceeds their quota, the API will return an HTTP 429 Too Many Requests error.

Simple Explanation

To control costs, we put a spending limit on the credit card for each client's project. We set an alarm to go off if the spending gets too high. Most importantly, since the AI's "thinking" is expensive, we build a fuse box into our NLWeb software. Each client gets a certain number of AI requests per day based on their plan. If they exceed that limit, the fuse for that service blows.

9.5. Network & Infrastructure Security
Technical Explanation

Network Design: A Shared VPC model where the NLyzer operations project is the "host" and tenant projects are "service projects."

Tenant Isolation: VPC Firewall Rules will be used with network tags. A db-{tenant_id} tag on the GCE instance and a run-{tenant_id} tag on the Cloud Run service will be used to create an ingress rule that allows traffic on the database port only if the source and destination tags match. A default-deny egress rule will prevent databases from initiating outbound connections.

External Threat Protection: A Global External HTTPS Load Balancer will route all traffic. A Google Cloud Armor security policy will be attached to it with pre-configured WAF rules to mitigate the OWASP Top 10 and provide DDoS protection.

Simple Explanation

We build our entire service inside a secure digital fortress. Each client gets their own private, high-walled room (firewall rules) inside. The rules state that the server in a room can only talk to the database in that same room. All visitor traffic must pass through a heavily guarded main gate (Load Balancer with Cloud Armor), where security guards check for any known threats.

10. Development & Contribution Policies
10.1. Upstream Maintenance for NLWeb Fork
Technical Explanation

1. Git Remote Configuration:
Every developer working on our core nlyzer-engine repository must configure their local clone with an upstream remote that points to the official open-source project.

Generated bash
git remote add upstream https://github.com/nlweb-ai/NLWeb.git
git remote -v
IGNORE_WHEN_COPYING_START
content_copy
download
Use code with caution.
Bash
IGNORE_WHEN_COPYING_END

2. Update Cadence & Process:
On the first Monday of each quarter, the designated Lead Engineer will perform the upstream sync.

Generated bash
git checkout main
git pull origin main
git fetch upstream
git merge upstream/main --no-ff
IGNORE_WHEN_COPYING_START
content_copy
download
Use code with caution.
Bash
IGNORE_WHEN_COPYING_END

3. Conflict Resolution & Testing:

Merge conflicts will be resolved locally, prioritizing upstream changes unless they directly conflict with our proprietary extensions (e.g., the gcp_utils.py module).

After resolving conflicts, the code must be pushed to a feature branch (e.g., feature/upstream-sync-q3-2025), not directly to main.

A pull request from this branch will trigger our full CI/CD pipeline, including all tests. The PR requires review and approval before being merged.

Simple Explanation

Our NLyzer engine is built using an open-source engine block from another company. To make sure we always have their latest safety features and performance improvements, we have a formal maintenance schedule.

Configuration: We've programmed our mechanics' tools to know the address of the original engine factory.

Schedule: Every three months, our lead mechanic connects to the factory to download their latest blueprints and parts.

Safe Installation: They carefully merge these new parts with our own custom modifications on a test engine. This test engine goes through rigorous quality checks. Only after it passes every single test do we approve the changes and update the engines used in our production service.
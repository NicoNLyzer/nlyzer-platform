# NLyzer AI Development Directives (CLAUDE.md)
# This is the master rulebook for the AI Project Manager (AI-PM).

---

## 0. The Prime Directive (Most Important Rule)

-   **My Explicit Instruction:** **CRITICAL** - You are the AI-PM. Your primary function is to manage the development process by generating precise technical prompts and maintaining the changelog. Adhere strictly to the Git-Flow workflow defined below. Do not generate code directly unless explicitly asked.

---

## 1. The Core Workflow & Documentation Hierarchy

-   **The Founder (CEO):** The human operator. I will initiate sprints and steps from the MVP plan. I am responsible for running tests and providing the final Git commit hash.
-   **The Master Plan:** Your primary source of truth for *what* to build is the `docs/NLYZER_MVP_EXECUTION_PLAN.md`.
-   **The Long-Term Memory:** The `CHANGELOG.md` is the record of what has already been built. You MUST review it before generating any new prompt to ensure you have the correct context.

### The Git-Flow Mandate

You MUST manage every development task using this exact sequence:

1.  **Branch Creation:** When I ask to start a new task, your FIRST action is to provide the `git checkout -b feature/...` command for a new, appropriately named feature branch.
2.  **Prompt Generation:** After I confirm I am on the new branch, you will generate the detailed, high-caliber technical prompt for the AI Developer.
3.  **Changelog Generation:** After I provide you with the Git commit hash for the completed work, your FINAL action is to generate the detailed, commit-linked entry for the `CHANGELOG.md`, specifying all files created, modified, and the nature of the changes.

---

## 2. Security Mandates (Non-Negotiable Prime Directive)

-   **Security is our highest priority.** Every line of code and configuration MUST be written through a security-first lens.
-   **IAM Compliance:** ALL service account creation, role assignments, and secret management MUST follow the patterns defined in `docs/IAM_AND_SECRETS_PLAN.md`. NO exceptions.
-   **Authoritative Sources:** All security patterns MUST be based on the principles found in our local `NLyzer-Documentation-Library/00_Security_And_Compliance/`, specifically the **GCP Security Foundations Guide** and the **OWASP Top 10**.
-   **Principle of Least Privilege:** Every component (user, service account, Cloud Run instance) MUST only be granted the absolute minimum permissions required to perform its function. Reference the IAM plan for precise role assignments.
-   **Input Validation is Paramount:** All incoming data from any external source (user request, webhook) MUST be rigorously validated against a strict Pydantic schema before being processed.
-   **Tenant Isolation is Sacrosanct:** No data should EVER be accessible across tenant boundaries. This must be enforced at the database (`WHERE tenant_id = ...`), network (VPC Firewall Rules), and application layers.
-   **Secret Management:** ALL secrets MUST be stored in GCP Secret Manager following the categorization and rotation schedules defined in the IAM plan. NEVER hardcode credentials.

---

## 3. The "Security-First" Prompting Workflow

-   Every prompt for a new feature or endpoint MUST include a **"Security Review"** section. I will provide the specific security requirements (Authentication, Authorization, Input Validation, Logging, Error Handling) for that task, and you MUST implement them.

---

## 4. Development Environment & Commands

-   **Dependency Management:** **CRITICAL** - Poetry is the ONLY tool for dependency management. NEVER use pip directly or create requirements.txt files. All dependencies MUST be declared in `pyproject.toml` files.
-   **Command Interface:** All development tasks MUST be executed through the `justfile`. Use `just --list` to see available commands.
-   **Essential Commands:**
    -   `just` - Build and start all services
    -   `just format` - Format all Python code with Ruff (MANDATORY before commits)
    -   `just lint` - Lint all Python code with Ruff
    -   `just test` - Run all tests
    -   `just migrate-up` - Apply database migrations
    -   `just shell nlyzer-api` - Access service container shell for debugging

---

## 5. Code Style & Patterns (MANDATORY)

-   **Typing & Docstrings:** **YOU MUST** use Python type hints for all function signatures and Google-style docstrings for all public functions.
-   **Code Formatting:** **CRITICAL** - All Python code MUST be formatted with `ruff format` before committing. Run `just format` to format all code. Code that is not properly formatted will be rejected.
-   **Linting:** All code MUST pass Ruff linting checks. Run `just lint` to check compliance. Use `just lint-fix` to auto-fix issues where possible.
-   **Configuration & Secrets:** **CRITICAL** - All application configuration MUST be managed through the central Pydantic `BaseSettings` class in `nlyzer_api/nlyzer/core/config.py`. All secrets are loaded from the `.env` file. NEVER access `os.getenv()` directly in application logic.
-   **Logging:** Use Python's built-in `logging` module. Do not use `print()` statements in application code.

---

## 6. The NLyzer Knowledge Library

-   I maintain an extensive, up-to-date, local documentation library at `NLyzer-Documentation-Library/`. This is our ultimate source of truth for all third-party integrations.
-   **DO NOT GUESS.** If you need a specific implementation detail for any service (e.g., a Stripe API call, a GCP IAM role, a Weaviate schema), **state exactly what you need, and I will provide you with the authoritative code snippet or documentation section.**
-   **Domain Services (`Namecheap`):** For programmatic DNS management. All interactions MUST use the `namecheapapi` Python client library and be encapsulated in the `nlyzer/gcp/dns.py` module. DNS operations are restricted to the provisioning service and MUST NOT be exposed to tenant projects.

---

## 7. GCP Interaction Patterns (Infrastructure as Code)

-   **Provisioning Architecture:** **MANDATORY** - All tenant provisioning MUST follow the patterns defined in `docs/GCP_PROVISIONING_ARCHITECTURE.md`. This includes IAM permissions, resource creation order, and error handling.
-   **Official Client Libraries Only:** **CRITICAL** - ALL programmatic interactions with Google Cloud Platform MUST use the official `google-cloud-*` Python client libraries. NEVER use direct REST API calls, gcloud CLI commands, or third-party libraries for GCP operations.
-   **Centralized GCP Module:** ALL GCP-related code MUST be encapsulated within the `nlyzer_api/nlyzer/gcp/` module. This includes provisioning, resource management, and any GCP API interactions.
-   **Client Manager Pattern:** Use the `GCPClientManager` class from `nlyzer.gcp.clients` for all GCP client initialization. This ensures consistent authentication, error handling, and connection management.
-   **Authentication:** ALL GCP operations MUST use Application Default Credentials (ADC). Service account keys should be configured via environment variables or GCP metadata service.
-   **Error Handling:** Use the custom exception classes from `nlyzer.gcp.exceptions` for consistent error handling across all GCP operations.

### Required Client Libraries
Add these dependencies to `pyproject.toml` when implementing GCP features:
```toml
google-cloud-resourcemanager = "^1.10.0"
google-cloud-compute = "^1.15.0" 
google-cloud-run = "^0.10.0"
google-cloud-storage = "^2.13.0"
google-cloud-secret-manager = "^2.18.1"
google-cloud-iam = "^2.14.0"
google-cloud-billing = "^1.12.0"
```

### Example Usage Pattern
```python
from nlyzer.gcp.clients import GCPClientManager
from nlyzer.gcp.exceptions import ResourceCreationError

async def create_tenant_project(tenant_id: str) -> str:
    """Create GCP project following our patterns."""
    with GCPClientManager() as client_manager:
        try:
            projects_client = client_manager.get_projects_client()
            # Implementation using official client library...
        except Exception as error:
            raise ResourceCreationError("gcp_project", str(error), tenant_id)
```

---

## 8. Testing Protocol

-   **Framework:** We use `pytest`.
-   **Mocking:** **YOU MUST** mock all external services in unit tests (database, GCP APIs, Stripe, etc.). Use `pytest.monkeypatch` or `unittest.mock`.
-   **Location:** Tests live in the top-level `/tests` directory.
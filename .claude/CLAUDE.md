Of course. This is a perfect time to refine your CLAUDE.md. Creating a detailed, directive-filled file now will save you countless hours of frustration later. It turns the AI from a generalist coder into a specialist for your project.

Based on your tech stack (GCP, Stripe, Python/FastAPI) and the excellent Anthropic guidelines, here is a refined, battle-ready CLAUDE.md file. It's designed to be a comprehensive set of instructions that covers the full lifecycle of your development process.

Copy this entire block and replace the content of your CLAUDE.md file.

Generated markdown
# NLyzer AI Development Directives (CLAUDE.md)
# Last Updated: 2025-07-27

This is the central rulebook for our project. You MUST adhere to these guidelines in all responses. The README.md contains the project vision; this file contains the rules for building it.

---

## 1. Core Directives & Principles

- **My Explicit Instruction:** **IMPORTANT** - Do not change, add, or remove anything I did not explicitly ask for. Only perform the exact task I have given you. Do not add placeholder comments like `# Add other logic here`.
- **Primary Tech Stack:** Our stack is FastAPI (Python 3.10+), PostgreSQL with pgvector, Redis, and a vector database like Qdrant or Pinecone. All Python code MUST be asynchronous (`async`/`await`).
- **Cloud Platform:** We use **Google Cloud Platform (GCP)**. When generating deployment scripts, IAM roles, or infrastructure-as-code, assume GCP services (e.g., Cloud Run, Secret Manager, Cloud SQL).
- **Architectural Bible:** The `README.md` file is the source of truth for our architecture. All business logic MUST be encapsulated within the appropriate agent as defined in the README.

---

## 2. Development Environment & Commands

### Environment Setup
- **Virtual Environment:** We use `venv` for environment management.
  - `python3 -m venv venv`
  - `source venv/bin/activate`
- **Install Dependencies:**
  - `pip install -r requirements.txt`

### Common Commands
- **Run Local Dev Server:**
  - `uvicorn nlyzer.main:app --reload`
  - This starts the FastAPI server with auto-reloading.
- **Run Tests:**
  - `pytest -v`
  - Runs the entire test suite.
- **Database Migrations:** (Using Alembic)
  - `alembic revision --autogenerate -m "Add new table"`
  - `alembic upgrade head`

---

## 3. Code Style & Patterns (MANDATORY)

- **Typing:** **YOU MUST** use Python type hints for all function signatures (parameters and return values).
- **Docstrings:** Use Google-style docstrings for all public functions and classes.
  ```python
  def my_function(param1: int) -> str:
      """This is a summary of the function.

      Args:
          param1: A description of the first parameter.

      Returns:
          A description of what the function returns.
      """
      return "hello"


Configuration & Secrets: CRITICAL - All configuration, especially secrets (API keys, DB URLs), MUST be loaded from environment variables. We use Pydantic's BaseSettings for this. NEVER hardcode a secret or key.

Create a nlyzer/core/config.py file to manage settings.

Dependencies: When you add a new library, immediately add it to the requirements.txt file.

Logging: Use Python's built-in logging module. Do not use print() statements for debugging in application code.

In every HTML file each DIV tag has a unique ID I can use to communicate with Claude THIS IS MANDATORY OFR DEBUGGING.


## 4. Key Files & Architectural Pointers

nlyzer/main.py: The main FastAPI application entry point. Handles middleware and top-level routers.

nlyzer/agents/: Business Logic Lives Here. Each file corresponds to a specific Commerce Agent from the README.

nlyzer/core/: Contains shared logic like the ConversationManager, Pydantic models, and database clients.

nlyzer/api/: Contains FastAPI routers that expose agent functionalities as HTTP endpoints.

nlyzer/integrations/: Contains all third-party API clients (Stripe, Weather APIs, etc.).

README.md: Contains the "what" and "why" of the business.

CLAUDE.md: (This file) Contains the "how" of the implementation.

## 5. Security Mandates (Non-Negotiable)

Tenant Isolation: CRITICAL - Every single database query that accesses tenant-specific data (like Products or Conversations) MUST be filtered by store_id (or tenant_id). There are absolutely no exceptions.

Input Validation: All incoming data from API requests (body, query params) MUST be validated using Pydantic models before being used. This is our first line of defense against injection attacks.

Authentication: API endpoints must be protected using FastAPI's Depends with security schemes (e.g., OAuth2). Clearly separate public endpoints from protected ones.

Stripe Integration: All Stripe logic, especially handling webhooks and using the secret key, MUST be on the backend. Create a dedicated webhook endpoint in nlyzer/api/webhooks.py that validates the Stripe signature.

## 6. Testing Protocol

Framework: We use pytest.

File Location: Tests live in a top-level /tests directory that mirrors the nlyzer/ app structure (e.g., tests/agents/test_visual_discovery.py).

Mocking: YOU MUST mock all external services in unit tests. This includes database calls, OpenAI APIs, Stripe APIs, and any service in the integrations folder. Use pytest.monkeypatch or unittest.mock.

Test Naming: Test functions must start with test_.

## 7. The NLyzer Knowledge Library

I maintain a comprehensive local `/Documentation` library with provider-specific docs, source code, and API references. This is our ultimate source of truth.

**DO NOT GUESS.** If you need a specific implementation detail for any of the following, **state what you need and I will provide you with the exact code snippet or documentation section.**

-   **Platform Integrations (`01_Platform_Integrations`):** Shopify, WooCommerce, etc. Ask for specific API client patterns.
-   **Core Technologies (`02_Core_Technologies`):** FastAPI, Pydantic, SQLAlchemy. Ask for advanced usage or specific function signatures.
-   **Infrastructure (`03_Infrastructure`):** GCP (Cloud Run, Secret Manager), Docker. Ask for deployment configurations or IAM roles.
-   **External Services (`05_External_Services`):** Stripe, OpenAI. Ask for specific API call examples, especially for complex features like Stripe's usage-based billing.
-   **Search Engine (`07_Core_Product`):** NLWeb. Ask for details on configuring LLM providers or retrieval systems.
-   **SRE (`08_Monitoring_SRE`):** Ask for patterns related to SLOs or error budgets.
# NLyzer AI Development Guide & Constitution

## 1. YOU MUST FOLLOW THESE CORE DIRECTIVES
- **ZERO DEVIATION:** My instructions are absolute. Do not change, add, or remove anything I did not explicitly ask for. Perform ONLY the assigned task. Acknowledge this rule in your response.
- **SECURITY IS PARAMOUNT:** Tenant data isolation is our most important principle. Every database query that touches user or product data MUST be filtered by `store_id`. Assume every API endpoint is public and requires authentication and authorization checks.
- **ARCHITECTURE FIRST:** Always reference the agent-based architecture defined in `README.md`. All business logic must be encapsulated within the appropriate agent (`VisualDiscoveryAgent`, `DestinationCommerceAgent`, etc.).
- **ASK IF UNSURE:** If a request is ambiguous or contradicts a previous rule, ask for clarification before writing code.

---

## 2. PROJECT ARCHITECTURE & KEY FILES
- **`README.md`**: Contains the full business and technical vision. This is our North Star.
- **`CLAUDE.md`**: (This file) Contains our development rules and guidelines.
- **`nlyzer/`**: The main Python application source code.
    - **`agents/`**: The brain of our application. Each file is a specialized agent (e.g., `visual_discovery.py`).
    - **`core/`**: Shared business logic and engine components (e.g., `conversation_manager.py`).
    - **`api/`**: FastAPI endpoints that expose the agent functionalities.
    - **`intelligence/`**: Services that connect to external data sources (e.g., weather, cultural DBs).
    - **`integrations/`**: Logic for connecting to third-party platforms like Shopify.
- **`instructions/`**: Contains markdown files with detailed examples and prompts for complex features.

---

## 3. TECHNOLOGY STACK & STYLE GUIDE
- **Primary Stack**: Python 3.10+, FastAPI, PostgreSQL with pgvector, Redis, and Qdrant/Pinecone.
- **Asynchronous Code**: **Everything is `async/await`**. Use `aiohttp` for external API calls. Do not use the `requests` library.
- **Code Formatting**: All Python code **MUST** be formatted with the `black` code formatter. All imports **MUST** be sorted with `isort`.
- **Data Validation**: Use Pydantic models for ALL API request and response bodies. This is a FastAPI best practice.
- **Dependencies**: All Python dependencies must be listed in `requirements.txt`.

---

## 4. DEVELOPMENT & GIT WORKFLOW
- **Branching Strategy**:
    - `feat/feature-name`: For new features (e.g., `feat/destination-agent`).
    - `fix/bug-description`: For bug fixes (e.g., `fix/image-upload-error`).
    - `chore/task-name`: For non-code tasks (e.g., `chore/update-readme`).
- **Commit Messages**: Write descriptive, imperative-mood commit messages.
    - GOOD: `Feat: Add initial DestinationCommerceAgent structure`
    - BAD: `added stuff`
- **Workflow**: Always create a new branch for each task. Do not commit directly to `main`.

---

## 5. COMMON COMMANDS & SCRIPTS
- **Setup Virtual Environment**:
  ```bash
  python -m venv venv
  source venv/bin/activate  # On macOS/Linux
  # venv\Scripts\activate  # On Windows
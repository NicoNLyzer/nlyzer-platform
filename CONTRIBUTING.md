# Contributing to NLyzer Platform

Welcome to the NLyzer platform development team! This document provides the essential information you need to get started and maintain our codebase.

---

## 🚀 Getting Started: The Developer's Golden Path

Follow these exact steps in order to set up your local development environment:

### Prerequisites
- Docker Desktop installed and running
- Git configured with your GitHub credentials
- Python 3.10+ installed locally (for tooling)

### Step-by-Step Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/NicoNLyzer/nlyzer-platform.git
   cd nlyzer-platform
   ```

2. **Create your environment configuration:**
   ```bash
   cp .env.example .env
   ```

3. **Populate the `.env` file with required secrets:**
   Open `.env` in your editor and fill in the following required values:
   - `DATABASE_URL` - PostgreSQL connection string
   - `REDIS_URL` - Redis connection string  
   - `OPENAI_API_KEY` - Your OpenAI API key
   - `STRIPE_SECRET_KEY` - Stripe API key (for billing)
   - `GCP_PROJECT_ID` - Your GCP project identifier
   - `SECRET_KEY` - A secure random string for JWT signing

4. **Build the Docker images:**
   ```bash
   docker-compose build
   ```

5. **Start the development environment:**
   ```bash
   docker-compose up
   ```

6. **Verify the services are running:**
   - NLyzer API: http://127.0.0.1:8000/docs
   - NLWeb Engine: http://127.0.0.1:8001
   - PostgreSQL: localhost:5432
   - Redis: localhost:6379
   - Qdrant: localhost:6333

7. **Run database migrations (in a new terminal):**
   ```bash
   docker-compose exec nlyzer-api alembic upgrade head
   ```

8. **Run the test suite to verify setup:**
   ```bash
   docker-compose exec nlyzer-api pytest -v
   ```

### Troubleshooting

If you encounter issues:
- Ensure Docker Desktop is running and has sufficient resources allocated (8GB RAM minimum)
- Check that all required ports are available (8000, 8001, 5432, 6379, 6333)
- Review Docker logs: `docker-compose logs -f [service-name]`

---

## 🔄 Upstream Maintenance for NLWeb Fork

We maintain a custom fork of the open-source NLWeb engine. This section defines our process for keeping our fork synchronized with upstream updates.

### Initial Setup (One-time per developer)

1. **Navigate to the nlweb_extension directory:**
   ```bash
   cd nlweb_extension
   ```

2. **Add the upstream remote:**
   ```bash
   git remote add upstream https://github.com/nlweb-ai/NLWeb.git
   git remote -v  # Verify remotes are configured correctly
   ```

   Expected output:
   ```
   origin    git@github.com:NicoNLyzer/nlyzer-engine.git (fetch)
   origin    git@github.com:NicoNLyzer/nlyzer-engine.git (push)
   upstream  https://github.com/nlweb-ai/NLWeb.git (fetch)
   upstream  https://github.com/nlweb-ai/NLWeb.git (push)
   ```

### Quarterly Sync Process

**Schedule:** First Monday of each quarter (January, April, July, October)

**Designated Lead Engineer** performs the following:

1. **Create a sync branch:**
   ```bash
   git checkout main
   git pull origin main
   git checkout -b feature/upstream-sync-q[N]-[YYYY]
   ```

2. **Fetch and merge upstream changes:**
   ```bash
   git fetch upstream
   git merge upstream/main --no-ff
   ```

3. **Resolve conflicts:**
   - Prioritize upstream changes unless they directly conflict with our proprietary extensions
   - Key files to review carefully:
     - `nlweb/gcp_utils.py` (our custom GCP integration)
     - `nlweb/main.py` (our resilient startup logic)
     - `Dockerfile` (our production hardening)

4. **Test the merged code:**
   ```bash
   # Build the updated image
   docker build -t nlyzer-engine:test .
   
   # Run comprehensive test suite
   pytest tests/ -v
   
   # Perform integration testing
   docker-compose up --build nlweb-extension
   ```

5. **Create Pull Request:**
   ```bash
   git push origin feature/upstream-sync-q[N]-[YYYY]
   ```
   
   Create a PR with:
   - Title: "chore: Quarterly upstream sync Q[N] [YYYY]"
   - Description listing all upstream changes incorporated
   - Any conflict resolutions explained
   - Test results summary

6. **Review and Merge:**
   - PR requires review from at least one other senior engineer
   - All CI/CD checks must pass
   - Deploy to staging environment for 24-hour soak test before production

### Emergency Security Updates

If upstream releases a critical security patch:
1. Follow the same process but on an expedited timeline
2. Create branch named `hotfix/upstream-security-[DATE]`
3. Bypass quarterly schedule with approval from Tech Lead

---

## 📝 Code Style Guidelines

Please refer to the `CLAUDE.md` file for detailed coding standards and patterns.

## 🔒 Security Requirements

All code must comply with the security mandates outlined in:
- `CLAUDE.md` - Security-first development practices
- `docs/UNIFIED_ARCHITECTURAL_BLUEPRINT.md` - Security architecture
- `NLyzer-Documentation-Library/00_Security_And_Compliance/` - Security references

## 🧪 Testing Requirements

- All new features must include unit tests
- Maintain minimum 80% code coverage
- Mock all external services in tests
- Run tests before pushing: `docker-compose exec nlyzer-api pytest -v`

## 📦 Submitting Changes

1. Create a feature branch from `main`
2. Make your changes following our guidelines
3. Ensure all tests pass
4. Submit a pull request with clear description
5. Address review feedback promptly

---

*For architectural decisions and detailed technical specifications, always refer to the [Unified Architectural Blueprint](./docs/UNIFIED_ARCHITECTURAL_BLUEPRINT.md).*
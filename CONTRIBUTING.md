# Contributing to NLyzer Platform

Welcome to the NLyzer platform development team! This document is your definitive guide for setting up, developing, and contributing to the project.

---

## 🚀 Getting Started: The Developer's Golden Path

Follow these steps to get your development environment running in under 5 minutes.

### Prerequisites
- Docker Desktop installed and running (8GB RAM minimum allocated)
- Git configured with your GitHub credentials
- [Just](https://github.com/casey/just) command runner installed
  ```bash
  # macOS
  brew install just
  
  # Linux
  curl --proto '=https' --tlsv1.2 -sSf https://just.systems/install.sh | bash -s -- --to /usr/local/bin
  ```

### Quick Start (One Command!)

```bash
# Clone and start everything
git clone https://github.com/NicoNLyzer/nlyzer-platform.git
cd nlyzer-platform
just quickstart
```

That's it! The `quickstart` command will:
1. Copy `.env.example` to `.env`
2. Build all Docker images
3. Start all services
4. Run database migrations
5. Perform health checks

### Manual Setup (Step-by-Step)

If you prefer to understand each step:

1. **Clone the repository:**
   ```bash
   git clone https://github.com/NicoNLyzer/nlyzer-platform.git
   cd nlyzer-platform
   ```

2. **Set up environment variables:**
   ```bash
   just env-setup
   # Edit .env with your actual API keys and secrets
   ```

3. **Start the development environment:**
   ```bash
   just  # Builds and starts all services
   ```

4. **Run database migrations:**
   ```bash
   just migrate
   ```

5. **Verify everything is working:**
   ```bash
   just health
   ```

### Available Services

Once running, you can access:
- **NLyzer API**: http://localhost:8000/docs (FastAPI Swagger UI)
- **NLWeb Engine**: http://localhost:8001
- **PostgreSQL**: localhost:5432
- **Redis**: localhost:6379
- **Qdrant**: localhost:6333

### Common Commands

All development tasks are managed through the `justfile`. Run `just` to see all available commands:

```bash
# Development
just            # Build and start all services
just stop       # Stop all services
just logs       # View logs for all services
just logs-service nlyzer-api  # View logs for specific service

# Testing
just test-api   # Run API tests
just test-nlweb # Run NLWeb tests
just test-all   # Run all tests

# Code Quality
just lint-py    # Lint Python code
just format-py  # Format Python code with Black

# Database
just migrate    # Run migrations
just migrate-create "description"  # Create new migration
just migrate-rollback  # Rollback last migration

# Utilities
just shell-api  # Access API container shell
just shell-db   # Access PostgreSQL shell
just clean      # Clean up Docker resources
```

---

## 💻 Development Workflow

### Branching Strategy

We follow a Git Flow-inspired branching model:

```
main            # Production-ready code
├── develop     # Integration branch for features
├── feature/*   # New features (from develop)
├── bugfix/*    # Bug fixes (from develop)
├── hotfix/*    # Emergency fixes (from main)
└── release/*   # Release preparation (from develop)
```

#### Creating a Feature Branch

```bash
git checkout develop
git pull origin develop
git checkout -b feature/your-feature-name

# Make your changes
just test-all  # Ensure tests pass
just lint-py   # Ensure code is properly formatted

git add .
git commit -m "feat: Add your feature description"
git push origin feature/your-feature-name
```

#### Branch Naming Conventions

- `feature/add-payment-integration`
- `bugfix/fix-login-validation`
- `hotfix/critical-security-patch`
- `release/v1.2.0`

### Commit Message Format

We follow [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>(<scope>): <subject>

<body>

<footer>
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks
- `perf`: Performance improvements

Examples:
```bash
git commit -m "feat(api): Add Stripe webhook handling"
git commit -m "fix(auth): Resolve JWT expiration issue"
git commit -m "docs: Update API endpoint documentation"
```

### Pull Request Process

1. **Create PR from your feature branch to develop**
2. **Ensure all checks pass:**
   - CI/CD pipeline (tests, linting, security scans)
   - Code coverage maintained above 80%
3. **Request review from at least one team member**
4. **Address review feedback**
5. **Squash and merge when approved**

### Documenting Decisions

When introducing new patterns or making architectural decisions:

1. **Check existing ADRs:**
   ```bash
   ls docs/adr/
   ```

2. **Create a new ADR if needed:**
   ```bash
   # Create next ADR number (e.g., 002)
   touch docs/adr/002-your-decision.md
   ```

3. **Follow the ADR template:**
   - Context: Why is this decision needed?
   - Decision: What are we doing?
   - Consequences: What are the trade-offs?

---

## 🔄 Upstream Maintenance for NLWeb Fork

We maintain a custom fork of the open-source NLWeb engine. This section defines our process for keeping it synchronized.

### Initial Setup (One-time per developer)

```bash
cd nlweb_extension
git remote add upstream https://github.com/nlweb-ai/NLWeb.git
git remote -v  # Verify remotes are configured
```

### Quarterly Sync Process

**Schedule:** First Monday of each quarter (January, April, July, October)

The designated Lead Engineer performs:

1. **Create sync branch:**
   ```bash
   git checkout main
   git pull origin main
   git checkout -b feature/upstream-sync-q1-2025
   ```

2. **Fetch and merge upstream:**
   ```bash
   git fetch upstream
   git merge upstream/main --no-ff
   ```

3. **Resolve conflicts:**
   - Prioritize upstream changes unless they conflict with our GCP integrations
   - Key files to review: `nlweb/gcp_utils.py`, `nlweb/main.py`, `Dockerfile`

4. **Test thoroughly:**
   ```bash
   just test-nlweb
   just rebuild nlweb-extension
   ```

5. **Create PR with detailed notes about changes incorporated**

### Emergency Security Updates

For critical security patches:
1. Follow same process on expedited timeline
2. Use branch name: `hotfix/upstream-security-YYYY-MM-DD`
3. Bypass quarterly schedule with Tech Lead approval

---

## 🔒 Security Requirements

### Before You Code

1. **Review security documentation:**
   - `CLAUDE.md` - Security mandates
   - `docs/UNIFIED_ARCHITECTURAL_BLUEPRINT.md` - Security architecture
   - `NLyzer-Documentation-Library/00_Security_And_Compliance/`

2. **Security checklist for new features:**
   - [ ] Input validation using Pydantic (see ADR 001)
   - [ ] Authentication required for endpoints
   - [ ] Rate limiting implemented
   - [ ] Tenant isolation enforced
   - [ ] Secrets in environment variables, not code
   - [ ] SQL injection prevention (use ORM)
   - [ ] XSS prevention (sanitize outputs)

### Security Testing

```bash
# Run security linter
docker-compose exec nlyzer-api bandit -r . -f json

# Check for dependency vulnerabilities
docker-compose exec nlyzer-api safety check

# Scan Docker images
trivy image nlyzer-api:latest
```

---

## 🧪 Testing Guidelines

### Test Structure

```
tests/
├── unit/           # Unit tests (mock external dependencies)
├── integration/    # Integration tests (use test database)
├── e2e/           # End-to-end tests (full stack)
└── fixtures/      # Shared test data and utilities
```

### Writing Tests

```python
# Example test following our patterns
import pytest
from unittest.mock import Mock, patch

@pytest.mark.asyncio
async def test_create_tenant_success():
    """Test successful tenant creation with mocked dependencies."""
    # Arrange
    mock_stripe = Mock()
    mock_gcp = Mock()
    
    # Act
    with patch('nlyzer_api.services.stripe_client', mock_stripe):
        with patch('nlyzer_api.services.gcp_client', mock_gcp):
            result = await create_tenant(...)
    
    # Assert
    assert result.status == "active"
    mock_stripe.create_customer.assert_called_once()
    mock_gcp.create_project.assert_called_once()
```

### Running Tests

```bash
# Run all tests
just test-all

# Run specific test file
docker-compose exec nlyzer-api pytest tests/unit/test_auth.py

# Run with coverage
docker-compose exec nlyzer-api pytest --cov=nlyzer_api --cov-report=html

# Run tests in watch mode
docker-compose exec nlyzer-api pytest-watch
```

---

## 📚 Additional Resources

### Project Documentation
- [Unified Architectural Blueprint](./docs/UNIFIED_ARCHITECTURAL_BLUEPRINT.md) - Complete technical architecture
- [Architectural Decision Records](./docs/adr/) - Documented technical decisions
- [API Documentation](http://localhost:8000/docs) - Interactive API documentation (when running)

### External Resources
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Docker Documentation](https://docs.docker.com/)
- [Google Cloud Platform Documentation](https://cloud.google.com/docs)
- [Pydantic Documentation](https://docs.pydantic.dev/)

### Getting Help

- **Slack Channel**: #nlyzer-dev
- **GitHub Issues**: [Report bugs or request features](https://github.com/NicoNLyzer/nlyzer-platform/issues)
- **Weekly Dev Sync**: Thursdays at 2 PM UTC

---

## 🎯 Quick Reference

### Most Used Commands

```bash
just            # Start everything
just stop       # Stop everything
just test-all   # Run all tests
just logs       # View all logs
just shell-api  # Access API shell
just migrate    # Run migrations
just clean      # Clean up
```

### Environment Variables

Critical variables that must be set in `.env`:
- `DATABASE_URL` - PostgreSQL connection
- `OPENAI_API_KEY` - For AI features
- `STRIPE_SECRET_KEY` - For billing
- `GCP_PROJECT_ID` - For cloud services

### Troubleshooting

**Services won't start:**
```bash
just clean
just env-check
just
```

**Database connection issues:**
```bash
just stop
docker-compose up -d postgres
just migrate
just
```

**Port conflicts:**
Check for processes using our ports:
```bash
lsof -i :8000  # API
lsof -i :8001  # NLWeb
lsof -i :5432  # PostgreSQL
```

---

*Thank you for contributing to NLyzer! Your code helps businesses worldwide leverage AI for conversational commerce.* 🚀
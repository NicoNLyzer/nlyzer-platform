# NLyzer Platform - MVP Command Runner
# Modern tooling with Poetry, Ruff, and Docker

# Default command: Build and start all services
default: build start

# Build all Docker images
build:
    @echo "Building Docker images..."
    docker-compose build

# Start all services in detached mode
start:
    @echo "Starting all services..."
    docker-compose up -d

# Stop and remove all services
stop:
    @echo "Stopping all services..."
    docker-compose down

# View the logs for all running services
logs:
    docker-compose logs -f

# View logs for a specific service
logs-service service:
    docker-compose logs -f {{service}}

# --- Code Quality ---
# Format all Python code with Ruff
format:
    @echo "Formatting Python code..."
    docker-compose run --rm nlyzer-api poetry run ruff format .
    docker-compose run --rm nlweb-extension poetry run ruff format .

# Lint all Python code with Ruff
lint:
    @echo "Linting Python code..."
    docker-compose run --rm nlyzer-api poetry run ruff check .
    docker-compose run --rm nlweb-extension poetry run ruff check .

# Fix linting issues automatically
lint-fix:
    @echo "Auto-fixing linting issues..."
    docker-compose run --rm nlyzer-api poetry run ruff check --fix .
    docker-compose run --rm nlweb-extension poetry run ruff check --fix .

# --- Testing ---
# Run all tests
test:
    @echo "Running all tests..."
    docker-compose run --rm nlyzer-api poetry run pytest -v
    docker-compose run --rm nlweb-extension poetry run pytest -v

# Run tests with coverage
test-cov:
    @echo "Running tests with coverage..."
    docker-compose run --rm nlyzer-api poetry run pytest --cov=nlyzer --cov-report=html --cov-report=term

# --- Database Migrations (for nlyzer-api) ---
# Create a new database migration file
migrate-make name:
    @echo "Creating new migration for nlyzer-api: {{name}}"
    docker-compose run --rm nlyzer-api poetry run alembic revision --autogenerate -m "{{name}}"

# Apply all database migrations
migrate-up:
    @echo "Applying database migrations for nlyzer-api..."
    docker-compose run --rm nlyzer-api poetry run alembic upgrade head

# Rollback last migration
migrate-down:
    @echo "Rolling back last migration..."
    docker-compose run --rm nlyzer-api poetry run alembic downgrade -1

# Show migration history
migrate-history:
    docker-compose run --rm nlyzer-api poetry run alembic history --verbose

# --- Development Utilities ---
# Install/update dependencies
deps:
    @echo "Installing dependencies..."
    docker-compose run --rm nlyzer-api poetry install
    docker-compose run --rm nlweb-extension poetry install

# Access the API shell
shell-api:
    docker-compose exec nlyzer-api /bin/bash

# Access the NLWeb shell
shell-nlweb:
    docker-compose exec nlweb-extension /bin/bash

# Access the PostgreSQL shell
shell-db:
    docker-compose exec postgres psql -U postgres -d nlyzer_db

# Clean up Docker resources
clean:
    @echo "Cleaning up Docker resources..."
    docker-compose down -v
    docker system prune -f

# Rebuild a specific service
rebuild service:
    @echo "Rebuilding {{service}}..."
    docker-compose build --no-cache {{service}}
    docker-compose up -d {{service}}

# Check service health
health:
    @echo "Checking service health..."
    docker-compose ps
    @echo "\nAPI Health Check:"
    curl -f http://localhost:8000/health || echo "API not responding"
    @echo "\nNLWeb Health Check:"  
    curl -f http://localhost:8001/health || echo "NLWeb not responding"

# --- Environment Setup ---
# Copy environment template
env-setup:
    @echo "Setting up environment file..."
    @test -f .env || cp .env.example .env
    @echo "✅ .env file created from template"
    @echo "📝 Please edit .env with your actual API keys and secrets"

# Validate environment configuration
env-check:
    @echo "Checking environment configuration..."
    @test -f .env || (echo "❌ Error: .env file not found. Run 'just env-setup' first." && exit 1)
    @echo "✅ .env file exists"
    @grep -q DATABASE_URL .env && echo "✅ DATABASE_URL configured" || echo "⚠️  DATABASE_URL not set"
    @grep -q OPENAI_API_KEY .env && echo "✅ OPENAI_API_KEY configured" || echo "⚠️  OPENAI_API_KEY not set"
    @grep -q STRIPE_SECRET_KEY .env && echo "✅ STRIPE_SECRET_KEY configured" || echo "⚠️  STRIPE_SECRET_KEY not set"

# --- Quick Commands ---
# Complete code quality check
quality: format lint test

# Full reset and restart
reset: clean env-setup build start migrate-up
    @echo "✅ Complete reset finished"
    @just health

# Quick start for new developers
quickstart: env-setup build start
    @echo "🚀 NLyzer Platform Quickstart Complete!"
    @echo ""
    @echo "Next steps:"
    @echo "1. Edit .env file with your API keys"
    @echo "2. Run 'just migrate-up' to set up the database"
    @echo "3. Run 'just health' to verify everything is working"
    @echo ""
    @echo "Available at:"
    @echo "📊 API Docs: http://localhost:8000/docs"
    @echo "🤖 NLWeb: http://localhost:8001"
    @echo ""
    @echo "Common commands:"
    @echo "• just logs     - View all service logs"
    @echo "• just test     - Run test suite"
    @echo "• just quality  - Format, lint, and test code"
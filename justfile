# NLyzer Platform - Command Runner
# This file provides a unified interface for all development tasks
# Run 'just' to see available commands

# Default command: Build images and start all services in detached mode
default:
    @echo "Building and starting all services..."
    docker-compose up --build -d

# Stop and remove all services
stop:
    @echo "Stopping all services..."
    docker-compose down

# View the logs for all running services
logs:
    docker-compose logs -f

# View the logs for a specific service (e.g., `just logs-service nlyzer-api`)
logs-service service:
    docker-compose logs -f {{service}}

# --- Testing ---
# Run the test suite for the main NLyzer API
test-api:
    @echo "Running nlyzer-api test suite..."
    docker-compose exec nlyzer-api pytest -v

# Run the test suite for the NLWeb Extension
test-nlweb:
    @echo "Running nlweb-extension test suite..."
    docker-compose exec nlweb-extension pytest -v

# Run all tests
test-all:
    @echo "Running all test suites..."
    docker-compose exec nlyzer-api pytest -v
    docker-compose exec nlweb-extension pytest -v

# --- Linting ---
# Lint all Python code
lint-py:
    @echo "Linting Python code..."
    docker-compose exec nlyzer-api ruff check .
    docker-compose exec nlweb-extension ruff check .

# Format Python code with Black
format-py:
    @echo "Formatting Python code..."
    docker-compose exec nlyzer-api black .
    docker-compose exec nlweb-extension black .

# --- Database Operations ---
# Run database migrations
migrate:
    @echo "Running database migrations..."
    docker-compose exec nlyzer-api alembic upgrade head

# Create a new migration
migrate-create name:
    @echo "Creating new migration: {{name}}"
    docker-compose exec nlyzer-api alembic revision --autogenerate -m "{{name}}"

# Rollback last migration
migrate-rollback:
    @echo "Rolling back last migration..."
    docker-compose exec nlyzer-api alembic downgrade -1

# --- Development Utilities ---
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
    @echo "\nAPI Health:"
    curl -s http://localhost:8000/health || echo "API not responding"
    @echo "\nNLWeb Health:"
    curl -s http://localhost:8001/health || echo "NLWeb not responding"

# --- Environment Setup ---
# Copy environment template
env-setup:
    @echo "Setting up environment file..."
    cp .env.example .env
    @echo "Please edit .env with your actual values"

# Validate environment variables
env-check:
    @echo "Checking required environment variables..."
    @test -f .env || (echo "Error: .env file not found. Run 'just env-setup' first." && exit 1)
    @grep -q "DATABASE_URL" .env || echo "Warning: DATABASE_URL not set"
    @grep -q "OPENAI_API_KEY" .env || echo "Warning: OPENAI_API_KEY not set"
    @grep -q "STRIPE_SECRET_KEY" .env || echo "Warning: STRIPE_SECRET_KEY not set"

# --- Documentation ---
# Serve documentation locally
docs-serve:
    @echo "Starting documentation server..."
    python -m http.server 8080 --directory docs/

# --- Quick Start ---
# One-command setup for new developers
quickstart: env-setup
    @echo "Starting NLyzer Platform quickstart..."
    @echo "1. Setting up environment..."
    @test -f .env || cp .env.example .env
    @echo "2. Building Docker images..."
    docker-compose build
    @echo "3. Starting services..."
    docker-compose up -d
    @echo "4. Running migrations..."
    sleep 5
    docker-compose exec nlyzer-api alembic upgrade head || echo "Migration pending - database may need initialization"
    @echo "5. Checking health..."
    @just health
    @echo "\n✅ Quickstart complete! Services are running."
    @echo "📝 Edit .env file with your actual API keys"
    @echo "🌐 API Docs: http://localhost:8000/docs"
    @echo "🤖 NLWeb: http://localhost:8001"
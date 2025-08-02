# NLyzer API Dockerfile - Optimized Multi-stage build with Poetry

# ============================================
# BUILDER STAGE - Full Python image with all build tools
# ============================================
FROM python:3.10 as builder

# Install Poetry
RUN pip install poetry

# Set Poetry configuration for optimal caching
ENV POETRY_NO_INTERACTION=1 \
    POETRY_VENV_IN_PROJECT=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

WORKDIR /app

# Copy Poetry configuration files
COPY pyproject.toml poetry.lock* ./

# Install all dependencies (including dev dependencies for complete environment)
RUN poetry install --with dev && rm -rf $POETRY_CACHE_DIR

# ============================================
# PRODUCTION STAGE - Minimal slim image
# ============================================
FROM python:3.10-slim as production

# Install system dependencies needed for runtime
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user for security
RUN useradd --create-home --shell /bin/bash appuser

# Set working directory
WORKDIR /home/appuser/app

# Copy virtual environment from builder stage
COPY --from=builder --chown=appuser:appuser /app/.venv /home/appuser/app/.venv

# Copy application code
COPY --chown=appuser:appuser . .

# Switch to non-root user
USER appuser

# Set PATH to include virtual environment
ENV PATH="/home/appuser/app/.venv/bin:$PATH" \
    PYTHONPATH="/home/appuser/app"

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Command to run the application
CMD ["uvicorn", "nlyzer.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
# NLWeb Extension Dockerfile - Multi-stage build with Poetry
FROM python:3.11-slim as builder

# Install Poetry
RUN pip install poetry

# Set Poetry configuration
ENV POETRY_NO_INTERACTION=1 \
    POETRY_VENV_IN_PROJECT=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

WORKDIR /app

# Copy Poetry files
COPY pyproject.toml poetry.lock* ./

# Install dependencies
RUN poetry install --only=main && rm -rf $POETRY_CACHE_DIR

# Production stage
FROM python:3.11-slim as production

# Create non-root user
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
ENV PATH="/home/appuser/app/.venv/bin:$PATH"

# Expose port
EXPOSE 8001

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8001/health || exit 1

# Command to run the application (placeholder - will be updated when NLWeb is integrated)
CMD ["python", "-m", "nlweb.main"]
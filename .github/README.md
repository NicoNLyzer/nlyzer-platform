# GitHub Actions - CI/CD Workflows

This directory contains GitHub Actions workflows for continuous integration and deployment.

## Workflows

### CI Pipeline
- Automated testing on pull requests
- Code quality checks (linting, formatting)
- Security scanning with CodeQL
- Dependency vulnerability scanning

### CD Pipeline  
- Automated deployment to staging on merge to main
- Production deployment with manual approval
- Docker image building and pushing to Artifact Registry
- Cloud Run service updates

## Configuration
Workflows use GitHub Secrets for sensitive values:
- `GCP_SA_KEY` - Service account key for GCP deployments
- `DOCKER_REGISTRY` - Artifact Registry URL
- `STRIPE_SECRET_KEY` - Stripe API key for testing

For detailed architecture, see [The Unified Architectural Blueprint](../docs/UNIFIED_ARCHITECTURAL_BLUEPRINT.md).
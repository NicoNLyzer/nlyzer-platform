# NLyzer Platform

> **NLyzer is a revolutionary Multimodal Conversational Commerce Platform. We provide "NLWeb-as-a-Service" to help businesses convert visual inspiration into sales.**

This repository contains the full source code for the NLyzer platform, including the control plane API, the extended NLWeb engine, and the marketing website.

---

## 🏛️ The Single Source of Truth: Our Architectural Blueprint

All development on this platform is governed by our master planning documents. These documents contain the complete technical architecture, deployment strategies, infrastructure provisioning, security plans, and frontend designs.

**Before starting any work, please review these definitive guides:**

-   **[The Unified Architectural Blueprint](./docs/UNIFIED_ARCHITECTURAL_BLUEPRINT.md)** - Complete technical architecture and 28-sprint roadmap
-   **[GCP Provisioning Architecture](./docs/GCP_PROVISIONING_ARCHITECTURE.md)** - Infrastructure as Code for automated tenant provisioning
-   **[IAM & Secrets Management Plan](./docs/IAM_AND_SECRETS_PLAN.md)** - Identity, access control, and secrets management strategy
-   **[Architectural Decision Records](./docs/adr/)** - Documented technical decisions and patterns

---

## 🚀 Getting Started: Local Development

This project uses Docker and Docker Compose to manage a consistent, multi-service local development environment with Poetry for dependency management.

### Prerequisites
-   Docker Desktop must be installed and running on your machine.
-   [Just](https://github.com/casey/just) command runner for unified task interface.
-   You must create a `.env` file from the `.env.example` template and populate it with the necessary secret keys.

### Quick Start

For new developers, run this single command to set up everything:

```bash
just quickstart
```

This will:
1. Copy `.env.example` to `.env`
2. Build all Docker images with Poetry
3. Start all services
4. Provide next steps for database setup

### Manual Setup

To build and start all services individually:

```bash
# Build and start all services
just

# Or use Docker Compose directly
docker-compose up --build
```

The main NLyzer API will be available at `http://localhost:8000/docs` (FastAPI Swagger UI), and the NLWeb instance will be at `http://localhost:8001`. The API services are configured with hot-reloading for immediate feedback during development.

### Running the Test Suite

```bash
# Run all tests
just test

# Run with coverage
just test-cov

# Format and lint code
just format
just lint
```

## 🛠️ Core Technologies

For the complete, up-to-date technology stack and architectural decisions, see **[The Unified Architectural Blueprint](./docs/UNIFIED_ARCHITECTURAL_BLUEPRINT.md)**.

### Key Components:
- **Backend**: Python 3.10+, FastAPI (async), Poetry for dependencies
- **AI Engine**: NLWeb (customized fork with GCP integrations)
- **Databases**: PostgreSQL (primary), Redis (cache), Qdrant/Weaviate (vector)
- **Infrastructure**: Google Cloud Platform (Cloud Run, GCE, Secret Manager)
- **Automated Provisioning**: GCP Infrastructure as Code via `nlyzer.gcp` module
- **Frontend**: Next.js 14 with TypeScript
- **Development**: Docker Compose, Just task runner, Ruff for linting

## 📁 Project Structure

This is a monorepo containing all components of the NLyzer platform:

```
NLyzer-Folder/
├── docs/                          # Architecture documentation
│   ├── UNIFIED_ARCHITECTURAL_BLUEPRINT.md
│   ├── GCP_PROVISIONING_ARCHITECTURE.md
│   └── adr/                       # Architectural Decision Records
├── nlyzer_api/                    # Control Plane API (FastAPI)
│   ├── nlyzer/
│   │   ├── agents/                # Business logic agents
│   │   ├── api/                   # FastAPI routers
│   │   ├── core/                  # Core utilities and config
│   │   ├── db/                    # Database models
│   │   └── gcp/                   # GCP provisioning module
│   │       ├── provisioning.py    # Tenant infrastructure automation
│   │       ├── clients.py         # GCP client management
│   │       └── exceptions.py      # Custom exceptions
│   ├── pyproject.toml             # Poetry dependencies
│   └── Dockerfile                 # Multi-stage build
├── nlweb_extension/               # Customized NLWeb fork
├── docker-compose.yml             # Local development stack
├── justfile                       # Unified command interface
├── .env.example                   # Environment template (236 variables)
├── CLAUDE.md                      # AI development directives
├── CONTRIBUTING.md                # Developer guide
└── README.md                      # This file
```

For detailed component descriptions, refer to **[The Unified Architectural Blueprint](./docs/UNIFIED_ARCHITECTURAL_BLUEPRINT.md)**.

## 🏗️ Automated Infrastructure Provisioning

NLyzer features a sophisticated Infrastructure as Code system for automated tenant provisioning on Google Cloud Platform.

### Key Features:
- **Complete Tenant Isolation**: Each tenant gets their own GCP project with strict security boundaries
- **Automated Resource Creation**: One-click provisioning of all required infrastructure
- **Enterprise Security**: Principle of least privilege IAM, Secret Manager integration
- **Self-Healing**: Automatic rollback on provisioning failures

### Provisioning Architecture:
The system automatically creates and configures:
1. **Isolated GCP Project** per tenant
2. **Weaviate Vector Database** on Google Compute Engine
3. **NLWeb AI Engine** deployed to Cloud Run
4. **Secure Networking** with VPC and firewall rules
5. **Configuration Storage** in Cloud Storage buckets
6. **Secrets Management** via Secret Manager

For complete details, see **[GCP Provisioning Architecture](./docs/GCP_PROVISIONING_ARCHITECTURE.md)**.

## 🔒 Security

Security is our highest priority. Every component follows enterprise security best practices:

### Identity & Access Management
- **7 Service Accounts** with least-privilege IAM roles across 3 project tiers
- **20+ Secrets** with automated rotation and tenant-specific isolation
- **Comprehensive IAM Strategy** documented in [IAM & Secrets Plan](./docs/IAM_AND_SECRETS_PLAN.md)

### Application Security
- **Input Validation**: Pydantic models for all API inputs (see [ADR 001](./docs/adr/001-pydantic-validation-patterns.md))
- **Tenant Isolation**: Complete data isolation at database, network, and project levels
- **Authentication**: JWT-based auth with configurable expiration
- **Secrets Management**: All credentials stored in Secret Manager with quarterly rotation
- **Audit Logging**: Comprehensive audit trails for compliance and forensics

### Infrastructure Security
- **Project-Level Isolation**: Each tenant gets their own GCP project
- **Network Segmentation**: VPC firewalls with tenant-specific tags
- **Conditional Access**: Time-based and IP-restricted service account policies
- **Emergency Procedures**: Documented incident response for compromised accounts

## 📚 Documentation

- **[Unified Architectural Blueprint](./docs/UNIFIED_ARCHITECTURAL_BLUEPRINT.md)** - Complete technical architecture
- **[GCP Provisioning Architecture](./docs/GCP_PROVISIONING_ARCHITECTURE.md)** - Infrastructure as Code design
- **[IAM & Secrets Management Plan](./docs/IAM_AND_SECRETS_PLAN.md)** - Identity and access control strategy
- **[CLAUDE.md](./CLAUDE.md)** - AI development directives and patterns
- **[CONTRIBUTING.md](./CONTRIBUTING.md)** - Developer onboarding guide
- **[Architectural Decision Records](./docs/adr/)** - Technical decisions and patterns

## 🚢 Deployment

The platform is designed for deployment on Google Cloud Platform with automated CI/CD pipelines. Each component is containerized and deployable independently:

- **Control Plane API**: Cloud Run with auto-scaling
- **NLWeb Instances**: Per-tenant Cloud Run services
- **Vector Databases**: GCE instances with persistent disks
- **Frontend**: Cloud CDN with global distribution

## 📝 License

Proprietary - NLyzer Platform © 2025. All rights reserved.
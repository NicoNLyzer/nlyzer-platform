# NLyzer Platform

> **NLyzer is a revolutionary Multimodal Conversational Commerce Platform. We provide "NLWeb-as-a-Service" to help businesses convert visual inspiration into sales.**

This repository contains the full source code for the NLyzer platform, including the control plane API, the extended NLWeb engine, and the marketing website.

---

## 🏛️ The Single Source of Truth: Our Architectural Blueprint

All development on this platform is governed by our master planning documents. These documents contain the complete technical architecture, deployment strategies, infrastructure provisioning, security plans, and frontend designs.

**Quick Links:**

-   **[The Unified Architectural Blueprint](./docs/UNIFIED_ARCHITECTURAL_BLUEPRINT.md)** - The definitive master plan for the entire platform (CISO approved, production ready).
-   **[The Grand Implementation Plan](./docs/GRAND_IMPLEMENTATION_PLAN.md)** - The step-by-step "Lego Instructions" for building the MVP with resolved dependencies.
-   **[The Changelog](./CHANGELOG.md)** - The commit-linked log of all development activities.
-   **[CEO Credential Collection Guide](./docs/CEO_CREDENTIAL_COLLECTION_GUIDE.md)** - Step-by-step guide for obtaining all required API keys and configurations.
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

To execute the backend test suite against the running containers, run the following command in a separate terminal:

```bash
just test-api
```

## 🛠️ Core Technologies

For the complete, up-to-date technology stack and architectural decisions, see **[The Unified Architectural Blueprint](./docs/UNIFIED_ARCHITECTURAL_BLUEPRINT.md)**.

### Key Components:
- **Backend**: Python 3.10+, FastAPI (async), Poetry for dependencies
- **AI Engine**: NLWeb (customized fork with GCP integrations)
- **Databases**: PostgreSQL (primary), Redis (cache), Qdrant (vector database - core MVP component)
- **Infrastructure**: Google Cloud Platform (Cloud Run, GCE, Secret Manager)
- **Automated Provisioning**: GCP Infrastructure as Code via `nlyzer.gcp` module with consolidated Sprint 4 deployment
- **Security**: Four critical security controls (Workload Identity, JWT auth, supply chain security, network security)
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
The system automatically creates and configures (Sprint 4 - Consolidated Deployment):
1. **Isolated GCP Project** per tenant
2. **Qdrant Vector Database** on Cloud Run (core MVP component)
3. **NLWeb AI Engine** deployed to Cloud Run with vector search integration
4. **Sales Agent Configuration** with Shopify integration and multimodal search
5. **Secure Networking** with VPC and firewall rules
6. **Configuration Storage** in Cloud Storage buckets
7. **Secrets Management** via Secret Manager with automated rotation

For complete details, see **[The Grand Implementation Plan](./docs/GRAND_IMPLEMENTATION_PLAN.md)** and **[The Unified Architectural Blueprint](./docs/UNIFIED_ARCHITECTURAL_BLUEPRINT.md)**.

## 🔒 Security

Security is our highest priority. The platform is **CISO approved** and implements enterprise security best practices with four critical security controls:

### Four Critical Security Controls (Mandatory)
1. **Workload Identity Federation**: Eliminates long-lived service account keys through secure impersonation
2. **Short-lived JWT Authentication**: Widget and API authentication using origin-bound tokens
3. **Supply Chain Security**: Image signing with Cosign and Binary Authorization verification
4. **Internal Network Security**: Service-to-service authentication and VPC egress controls

### Enterprise Security Framework
- **OWASP Top 10 Compliance**: Complete coverage of web application security risks
- **SOC 2 Type II Preparation**: Framework for security, availability, and confidentiality
- **Security Governance**: Incident response, threat detection, and compliance management
- **Continuous Monitoring**: Real-time security monitoring and automated alerting

### Identity & Access Management
- **Workload Identity Federation** with secure impersonation and audit logging
- **Principle of Least Privilege** with automated quarterly access reviews
- **Developer Workflow Security** with secure credential management and MFA enforcement
- **Service Account Management** with role-based access and conditional policies

### Application Security
- **Input Validation**: Pydantic models for all API inputs with comprehensive schema validation
- **Tenant Isolation**: Complete data isolation at database, network, and project levels
- **Authentication**: JWT-based auth with short-lived tokens and origin validation
- **Secrets Management**: All credentials stored in Secret Manager with automated rotation
- **Audit Logging**: Comprehensive audit trails for compliance and forensics

### Infrastructure Security
- **Project-Level Isolation**: Each tenant gets their own GCP project with strict boundaries
- **Network Segmentation**: VPC firewalls with tenant-specific tags and egress controls
- **Binary Authorization**: Container image verification with signature validation
- **Emergency Procedures**: Documented incident response for compromised accounts

## 📚 Documentation

- **[Unified Architectural Blueprint](./docs/UNIFIED_ARCHITECTURAL_BLUEPRINT.md)** - Complete technical architecture (CISO approved, production ready)
- **[Grand Implementation Plan](./docs/GRAND_IMPLEMENTATION_PLAN.md)** - Definitive MVP implementation guide with resolved dependencies
- **[CEO Credential Collection Guide](./docs/CEO_CREDENTIAL_COLLECTION_GUIDE.md)** - Step-by-step guide for obtaining all required API keys
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
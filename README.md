# NLyzer Platform

> **NLyzer is a revolutionary Multimodal Conversational Commerce Platform. We provide "NLWeb-as-a-Service" to help businesses convert visual inspiration into sales.**

This repository contains the full source code for the NLyzer platform, including the control plane API, the extended NLWeb engine, and the marketing website.

---

## 🏛️ The Single Source of Truth: Our Architectural Blueprint

All development on this platform is governed by our master planning document. This document contains the complete technical architecture, deployment strategies, data ingestion models, security plans, and frontend designs.

**Before starting any work, please review the definitive guide:**

-   **[The Unified Architectural Blueprint](./docs/UNIFIED_ARCHITECTURAL_BLUEPRINT.md)**

---

## 🚀 Getting Started: Local Development

This project uses Docker and Docker Compose to manage a consistent, multi-service local development environment.

### Prerequisites
-   Docker Desktop must be installed and running on your machine.
-   You must create a `.env` file from the `.env.example` template and populate it with the necessary secret keys.

### Running the Full Local Stack
To build the Docker images and start all services (NLyzer API, NLWeb Engine, PostgreSQL, Weaviate, etc.), run the following command from the project root:

```bash
docker-compose up --build
```

The main NLyzer API will be available at `http://127.0.0.1:8000`, and the NLWeb instance will be at `http://127.0.0.1:8001`. The API services are configured with hot-reloading for immediate feedback during development.

### Running the Test Suite
To execute the backend test suite against the running containers, run the following command in a separate terminal:

```bash
docker-compose exec nlyzer-api pytest -v
```

## 🛠️ Core Technologies

| Category | Technology | Purpose |
|----------|------------|---------|
| Backend | Python 3.10+, FastAPI | The NLyzer Control Plane API |
| Core Engine | NLWeb (Open Source) | The AI/Search Engine we deploy |
| Frontend | Next.js, React, Tailwind | Marketing website & Client-side widget |
| Database | PostgreSQL | Relational data (users, tenants) |
| Vector DB | Weaviate | Vector embeddings for semantic search |
| Cloud | Google Cloud Platform | All production infrastructure |
| Deployment | Docker, Cloud Run | Containerization & Serverless Compute |

## 📁 Project Structure
This is a monorepo containing all artifacts for the NLyzer platform.

```
nlyzer-platform/
├── .github/          # CI/CD Workflows
├── docs/             # Master Architectural Blueprints
├── nlyzer_api/       # The Python FastAPI Control Plane
├── nlweb_extension/  # Our extended version of the NLWeb Engine
├── website/          # The Next.js marketing website
├── scripts/          # Operational scripts (e.g., data ingestion)
├── tests/            # Integration tests
├── CLAUDE.md         # The AI Development Rulebook
└── README.md         # This file
```
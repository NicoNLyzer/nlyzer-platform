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

For the complete, up-to-date technology stack and architectural decisions, see **[The Unified Architectural Blueprint](./docs/UNIFIED_ARCHITECTURAL_BLUEPRINT.md)**.

Key technologies include Python/FastAPI for the backend, NLWeb as our core AI engine, Next.js for the frontend, and Google Cloud Platform for infrastructure.

## 📁 Project Structure

This is a monorepo containing all components of the NLyzer platform. For the detailed project structure and component descriptions, refer to **[The Unified Architectural Blueprint](./docs/UNIFIED_ARCHITECTURAL_BLUEPRINT.md)**.
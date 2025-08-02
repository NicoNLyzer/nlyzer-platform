# NLyzer API - Control Plane

This directory contains the FastAPI-based control plane for the NLyzer platform.

## Overview
The NLyzer API serves as the central orchestration layer, managing:
- User authentication and authorization
- Tenant provisioning and management
- Billing integration with Stripe
- Orchestration of NLWeb engine instances

## Structure
- `core/` - Core utilities (config, security, database)
- `api/` - FastAPI route handlers
- `models/` - SQLAlchemy database models  
- `schemas/` - Pydantic validation schemas
- `services/` - Business logic layer
- `main.py` - Application entry point

For detailed architecture, see [The Unified Architectural Blueprint](../docs/UNIFIED_ARCHITECTURAL_BLUEPRINT.md).
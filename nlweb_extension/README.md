# NLWeb Extension - Custom AI Engine

This directory contains our customized fork of the NLWeb engine with GCP-specific enhancements.

## Overview
Our extended NLWeb engine includes:
- GCP integration utilities for Cloud Storage and Secret Manager
- Resilient startup logic with health checks
- Multi-tenant configuration management
- System-level API endpoints for orchestration

## Key Modifications
- `nlweb/gcp_utils.py` - GCP service integrations
- `nlweb/main.py` - Enhanced startup and system endpoints
- `Dockerfile` - Production-hardened multi-stage build

## Upstream Sync
This fork is synchronized quarterly with the upstream NLWeb repository.
See [CONTRIBUTING.md](../CONTRIBUTING.md) for the maintenance process.

For detailed architecture, see [The Unified Architectural Blueprint](../docs/UNIFIED_ARCHITECTURAL_BLUEPRINT.md).
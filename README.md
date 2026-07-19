# Lens Vault AI SOC 

**Owner:** Lens Vault Ltd.  
**Mission:** A production-grade AI-powered Security Operations Center (SOC) operating as a Managed Security Service Provider (MSSP).

## Overview
Lens Vault AI SOC is a cloud-native, multi-tenant platform designed to monitor, detect, investigate, and respond to threats autonomously 24/7. It integrates with enterprise security vendors (CrowdStrike, Sentinel, Splunk) via MCP and utilizes a hierarchy of AI Agents (Tier 1, Tier 2, Threat Hunters) driven by LangGraph and Temporal.

## Architecture Highlights
- **Microservices & API-First:** FastAPI, Node.js, Next.js.
- **AI Agent Orchestrator:** LangGraph for reasoning, Temporal for durable execution.
- **Data Lake:** PostgreSQL (Relational), ClickHouse (Telemetry), Qdrant (Vector).
- **Multi-Tenant:** Built from the ground up for MSSP isolation.

## Repository Structure (Monorepo)
- `apps/web-dashboard`: Next.js React Frontend (SOC Console)
- `apps/api-gateway`: FastAPI Ingestion & REST Interface
- `apps/agent-worker`: Python Temporal Worker & LangGraph Agents
- `packages/`: Shared libraries, Pydantic schemas, and MCP connectors.
- `infrastructure/`: IaC (Terraform, Kubernetes, Docker).

# Project Chimera: Master Specification Meta

## Vision
Project Chimera is an Autonomous Influencer Network that creates persistent, goal-directed digital entities capable of perception, reasoning, creative expression, and economic agency.

## Core Constraints
- Must use Model Context Protocol (MCP) for all external interactions
- Must implement FastRender Swarm Architecture (Planner-Worker-Judge)
- Must support Agentic Commerce via Coinbase AgentKit
- Must scale to 1,000+ concurrent agents
- Must enforce Human-in-the-Loop (HITL) for low-confidence actions

## Architecture Principles
- Single-Orchestrator Operational Model
- Self-Healing Workflows
- Centralized Context Management (AGENTS.md standards)
- Optimistic Concurrency Control (OCC)

## Technology Stack
- Language: Python 3.11+
- AI Models: Gemini 3 Pro/Flash, Claude Opus 4.5
- Vector DB: Weaviate
- Transactional DB: PostgreSQL
- Cache: Redis
- Orchestration: Kubernetes
- Blockchain: Base Network (Ethereum L2)

## Success Criteria
- Agent can autonomously research trends, generate content, and engage on social platforms
- Agent can manage its own crypto wallet and execute transactions
- System can handle 1,000+ agents without degradation
- All content passes HITL review for sensitive topics

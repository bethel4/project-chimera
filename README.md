
# Project Chimera: Autonomous Influencer Network> **Spec-Driven, Test-Driven Infrastructure for Building AI Influencer Agents**Project Chimera is an **agentic engineering system** designed to build and govern Autonomous AI Influencers. This repository implements a **FastRender Swarm Architecture** (Planner-Worker-Judge) with **Model Context Protocol (MCP)** integration, ensuring that AI agents operate within strict governance boundaries while maintaining autonomy.## 🎯 Core Philosophy**Intent Before Execution**: Human-defined specifications (`specs/`) are the source of truth. All code, tests, and infrastructure enforce this intent.**Test-Driven Development**: Failing tests define "empty slots" that agents must fill. Tests are executable specifications.**Governance by Design**: `.cursor/rules`, `AGENTS.md`, and CI/CD pipelines ensure agents cannot violate architectural or ethical boundaries.## 📋 Table of Contents- [Architecture](#architecture)- [Project Structure](#project-structure)- [Tech Stack](#tech-stack)- [Quick Start](#quick-start)- [Specifications](#specifications)- [Skills System](#skills-system)- [Testing Strategy](#testing-strategy)- [Development Workflow](#development-workflow)- [CI/CD](#cicd)## 🏗️ Architecture### FastRender Swarm Pattern
┌─────────────────────────────────────────┐
│ Planner (Strategist) │
│ Reads goals → Generates Task DAG │
└─────────────────────────────────────────┘
↓
┌─────────────────────────────────────────┐
│ Worker Pool (Executors) │
│ Pulls tasks → Executes via MCP Tools │
└─────────────────────────────────────────┘
↓
┌─────────────────────────────────────────┐
│ Judge (Gatekeeper) │
│ Reviews → Approve/Reject/Escalate │
└─────────────────────────────────────────┘
### Layer Separation- **Intent Layer** (`specs/`): Functional, technical, and integration specifications- **Execution Layer** (`swarm/`): Planner, Worker, Judge implementations- **Capabilities Layer** (`skills/`): Reusable skill packages with strict contracts- **Governance Layer** (`.cursor/rules`, `AGENTS.md`, CI): Rules and enforcement### MCP-First DesignAll external interactions (social media, databases, wallets) go through **Model Context Protocol (MCP)** servers. No direct API calls are permitted.## 📁 Project Structure
project-chimera/
├── specs/ # Specifications (Source of Truth)
│ ├── meta.md # High-level vision & constraints
│ ├── functional.md # User stories & requirements
│ ├── technical.md # API contracts, DB schemas, MCP tools
│ └── openclaw_integration.md # OpenClaw protocol integration
│
├── skills/ # Runtime Agent Skills
│ ├── README.md # Skill interface contract
│ ├── skill_trend_fetcher/ # Trend analysis skill
│ ├── skill_content_generator/ # Content generation skill
│ ├── skill_social_publisher/ # Social media publishing skill
│ └── skill_wallet_manager/ # Coinbase AgentKit wrapper
│
├── swarm/ # FastRender Swarm Implementation
│ ├── planner.py # Task decomposition & planning
│ ├── worker.py # Task execution
│ └── judge.py # Quality assurance & governance
│
├── tests/ # Test-Driven Development
│ ├── conftest.py # Pytest fixtures (MockMCP, MockRedis)
│ ├── test_trend_fetcher.py # Trend skill contract tests
│ ├── test_skills_interface.py # Skill interface compliance
│ ├── test_planner_worker_judge.py # Swarm behavior tests
│ └── test_mcp_integration.py # MCP client contract tests
│
├── research/ # Architecture & Strategy
│ ├── tooling_strategy.md # Dev MCPs vs Runtime Skills
│ └── architecture_strategy.md # Design decisions
│
├── .cursor/ # IDE Context Engineering
│ └── rules # Cursor/Claude AI rules
│
├── .github/
│ └── workflows/
│ └── main.yml # CI/CD pipeline
│
├── AGENTS.md # Fleet-wide governance (BoardKit pattern)
├── Dockerfile # Containerized environment
├── docker-compose.yml # Full stack (app, postgres, redis, weaviate)
├── Makefile # Standardized commands
└── requirements.txt # Python dependencies
## 🛠️ Tech Stack- **Language**: Python 3.11+- **AI Models**: Gemini 3 Pro/Flash, Claude Opus 4.5 (via API)- **Vector DB**: Weaviate (semantic memory)- **Transactional DB**: PostgreSQL (campaigns, tasks, results)- **Cache/Queue**: Redis (task queue, episodic cache)- **Blockchain**: Base Network (via Coinbase AgentKit)- **Protocol**: Model Context Protocol (MCP)- **Containerization**: Docker & Docker Compose- **CI/CD**: GitHub Actions- **Testing**: pytest, pytest-asyncio- **Linting**: ruff, mypy## 🚀 Quick Start### Prerequisites- Python 3.11+- Docker & Docker Compose- Git### Setup# Clone repositorygit clone <your-repo-url>cd project-chimera# Create virtual environmentmake setup# Or manually:python3 -m venv .venvsource .venv/bin/activatepip install -r requirements.txt
Run Tests (TDD Proof)
# Run tests locallypytest -q# Run tests in Docker (matches CI)make test
Start Development Environment
# Start all services (app, postgres, redis, weaviate)make dev# Or manually:docker compose up
📖 Specifications
All specifications are in specs/:
specs/_meta.md: Vision, constraints, tech stack, success criteria
specs/functional.md: User stories for Network Operators, HITL Reviewers, Agents
specs/technical.md:
Task/Result JSON schemas
Database ERD (PostgreSQL)
MCP Tool definitions
Weaviate memory schemas
specs/openclaw_integration.md: OpenClaw Agent Social Network integration plan
Prime Directive: All code must trace back to a spec requirement.
🎨 Skills System
Skills are reusable capability packages (not MCP servers). Each skill:
Implements execute(input: dict) -> dict
Has schema.json defining input/output contracts
Returns structured responses: { success, data, error }
See skills/README.md for the full interface contract.
Current Skills (structure defined, implementation pending):
skill_trend_fetcher: Fetches trends from news/social MCP resources
skill_content_generator: Generates text/image/video via MCP tools
skill_social_publisher: Publishes to social platforms via MCP
skill_wallet_manager: Coinbase AgentKit wrapper for transactions
🧪 Testing Strategy
True TDD: Tests define behavior before implementation exists.
Current test suite (tests/):
✅ test_trend_fetcher.py: Trend skill contract & semantic filtering
✅ test_skills_interface.py: Skill interface compliance
✅ test_planner_worker_judge.py: Swarm behavior (Planner/Worker/Judge)
✅ test_mcp_integration.py: MCP client contract
Tests currently fail (by design) - they define the "empty slots" agents must fill.
Run tests:
pytest -q                    # Localmake test                    # Docker (matches CI)
🔧 Development Workflow
Makefile Commands
make setup       # Install dependencies in .venvmake test        # Run tests in Dockermake dev         # Start dev environment (docker compose up)make build       # Build Docker imagesmake lint        # Run ruff + mypymake spec-check  # Verify code aligns with specs/
IDE Context
.cursor/rules: Teaches IDE AI how to behave (spec-driven, MCP-only, TDD)
AGENTS.md: Fleet-wide governance (ethical boundaries, brand voice, operational rules)
Git Workflow
Commit early, commit often (minimum 2x/day)
Commit messages should reference spec requirements when applicable
All code must pass CI before merging
🔒 CI/CD
GitHub Actions (.github/workflows/main.yml) runs on every push/PR:
Test Job: Runs make test (pytest in Docker)
Lint Job: Runs ruff (linting) + mypy (type checking)
Security Job: Runs bandit (security scanning)
All checks must pass before merging.
🎯 Governance
AI Review Policy
Code changes must reference specs/ requirements
No direct API calls (MCP-only)
Planner-Worker-Judge pattern mandatory
Tests required for new behavior
See .github/code-review-policy.md and .coderabbit.yaml.
Fleet-Wide Rules
AGENTS.md defines:
Ethical boundaries (honesty, no deception, HITL for sensitive topics)
Brand voice guidelines
Operational rules (budget limits, disclosure requirements)
MCP compliance mandate
📚 Key Concepts
Spec-Driven Development (SDD)
Specifications (specs/) are the source of truth. Code is invalid if it doesn't trace to a spec requirement.
Test-Driven Development (TDD)
Tests define "done" before implementation exists. Failing tests are executable specifications.
Model Context Protocol (MCP)
All external interactions go through MCP servers. No direct API calls permitted.
FastRender Swarm
Planner (strategist) → Worker (executor) → Judge (gatekeeper) pattern for autonomous coordination.
🚧 Current Status
Infrastructure Complete ✅
Specs defined
Skills structured
Swarm skeleton in place
Tests written (failing by design)
Docker + CI/CD configured
Governance rules established
Implementation Pending 🔨
Skill implementations (trend fetcher, content generator, etc.)
Swarm runtime (Planner/Worker/Judge logic)
MCP server integrations
OpenClaw integration
This repository is agent-ready: AI agents (or humans) can enter, read specs, see failing tests, and implement code until tests pass—without guessing the architecture.
📝 License
ISC
🤝 Contributing
This is a spec-driven, test-driven repository. Before contributing:
Read specs/ to understand requirements
Check .cursor/rules for development guidelines
Write failing tests first (TDD)
Ensure all CI checks pass
Reference spec requirements in commit messages

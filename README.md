project-chimera/
├── specs/                     # Specifications (source of truth)
│   ├── _meta.md               # Vision, constraints, success criteria
│   ├── functional.md          # User stories and requirements
│   ├── technical.md           # Schemas, DB design, MCP tools
│   └── openclaw_integration.md
│
├── skills/                    # Runtime agent capabilities
│   ├── README.md              # Skill interface contract
│   ├── skill_trend_fetcher/
│   ├── skill_content_generator/
│   ├── skill_social_publisher/
│   └── skill_wallet_manager/
│
├── swarm/                     # FastRender Swarm roles
│   ├── planner.py
│   ├── worker.py
│   └── judge.py
│
├── tests/                     # Test-driven specifications
│   ├── conftest.py
│   ├── test_trend_fetcher.py
│   ├── test_skills_interface.py
│   ├── test_planner_worker_judge.py
│   └── test_mcp_integration.py
│
├── research/
│   ├── tooling_strategy.md
│   └── architecture_strategy.md
│
├── .cursor/
│   └── rules
│
├── .github/
│   └── workflows/
│       └── main.yml
│
├── AGENTS.md
├── Dockerfile
├── docker-compose.yml
├── Makefile
└── requirements.txt

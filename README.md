# text-to-sql-multi-agents

## Project structure

backend/
├── src/
│   ├── text_to_sql_agents/
│   │   ├── agents/                 # individual agents (SQL gen, guardrail, etc.)
│   │   ├── orchestration/          # MagenticManager & orchestration logic
│   │   ├── adapters/               # Azure SQL / BigQuery / Snowflake connectors
│   │   ├── guardrails/             # SQL safety validation logic
│   │   ├── models/                 # Pydantic schemas, config
│   │   ├── services/               # ⚡ new module: handles SK + Foundry connection
│   │   │   ├── __init__.py
│   │   │   ├── kernel_service.py   # creates & configures Semantic Kernel
│   │   │   ├── foundry_service.py  # manages Azure Foundry agent connection
│   │   │   ├── orchestrator_service.py  # wraps MagenticManager as SK skill
│   │   └── utils/                  # logs, plotting, etc.
│   │   ├── main.py                 # backend entrypoint (FastAPI)
│   ├── tests/
│   └── __init__.py
├── infra/
│   ├── Dockerfile
│   ├── foundry_agent.yaml
│   ├── azure_pipelines.yaml
│   └── README.md
└── pyproject.toml


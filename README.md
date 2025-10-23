# 🧩 Overview

This project implements a multi-agent system for intelligent data querying and visualization.
It uses Semantic Kernel as the orchestration backbone, integrates with Azure AI Foundry for agent execution, and supports multiple database backends including Azure SQL, BigQuery, and Snowflake.

# ✨ Key Features

- 🧠 Magentic multi-agent orchestration

SQL generation, validation, execution, summarization, and visualization.

- 🛡️ Guardrail system

Prevents unsafe SQL (e.g., DELETE, DROP, UPDATE).

- 🗄️ Pluggable database adapters

Azure SQL, BigQuery, and Snowflake ready.

- 🪄 Semantic Kernel + Azure Foundry integration

Enables dynamic agent coordination and context-aware reasoning.

- 📊 Automatic visualization & Power BI export

Generate matplotlib charts and Power BI reports on the fly.

💬 Frontend powered by Chainlit

Interactive chat UI for querying data using natural language.



## 🏗️ Project structure
```bash
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
```
## ⚙️ Configuration
All configuration is centralized in **src/text_to_sql_agents/config/settings.yaml**
```yaml
# src/text_to_sql_agents/config/settings.yaml

default:
  app:
    name: "Text-to-SQL Agent"
    environment: "development"
    log_level: "info"
    port: 8000

  azure:
    openai_endpoint: "https://shared-openai-resource.openai.azure.com/"
    openai_deployment: "gpt-4o"
    use_managed_identity: true
    foundry_agent_name: "text2sql-agent"

  database:
    provider: "azure_sql"
    azure_sql:
      server: "prod-sql-server.database.windows.net"
      database: "text2sql_prod"
      username: "sqladmin"
      password: "PROD_PASSWORD"

  orchestration:
    retry_max: 2
    enable_powerbi: true

  powerbi:
    workspace_id: "prod-workspace-id"
    dataset_name: "Text2SQL_Prod_Dataset"
    client_id: "prod-client-id"
    tenant_id: "prod-tenant-id"


development:
  app:
    name: "Text-to-SQL Agent (Dev)"
    log_level: "debug"
    port: 8000

  azure:
    openai_endpoint: "https://dev-openai-resource.openai.azure.com/"
    openai_deployment: "gpt-4o-mini"
    use_managed_identity: false
    foundry_agent_name: "text2sql-agent-dev"

  database:
    provider: "azure_sql"
    azure_sql:
      server: "dev-sql-server.database.windows.net"
      database: "text2sql_dev"
      username: "sqladmin"
      password: "DEV_PASSWORD"

  orchestration:
    retry_max: 3
    enable_powerbi: false

  powerbi:
    workspace_id: "dev-workspace-id"
    dataset_name: "Dev_Text2SQL_Dataset"
    client_id: "dev-client-id"
    tenant_id: "dev-tenant-id"


staging:
  app:
    name: "Text-to-SQL Agent (Staging)"
    log_level: "info"
    port: 8080

  azure:
    openai_endpoint: "https://staging-openai-resource.openai.azure.com/"
    openai_deployment: "gpt-4o"
    use_managed_identity: true
    foundry_agent_name: "text2sql-agent-staging"

```

# 🚀 Running the Backend
1. Create a virtual environment:
```bash
uv  venv 
```
2. Activate the virtual environment:
```bash
# Windows (PowerShell):
.\venv\Scripts\Activate
```
3. Install dependencies (with uv
)
```bash
uv sync
```

4. Start the FastAPI backend
```bash
uv run start
```

The API will be available at:
```
🌐 http://localhost:8000
```

Check health:
```
curl http://localhost:8000/health
```
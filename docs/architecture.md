```mermaid
flowchart TD
    %% --- User Input ---
    U[🧑‍💻 User Query<br/>("Show top 5 products by revenue")] -->|Natural language| A[🎯 SQL Generator Agent]

    %% --- SQL Generation + Guardrails ---
    A -->|Proposes SQL| G[🛡️ Guardrail Agent]
    G -->|Validate safety<br/>(SELECT-only, limit check)| V{Safe SQL?}

    %% --- Unsafe branch ---
    V -->|❌ No| E1[⚠️ Return Error<br/>"Unsafe query detected"]:::error

    %% --- Safe path ---
    V -->|✅ Yes| X[🧩 SQL Executor Agent]
    X -->|Run SQL<br/>via DB Adapter| D[(🗄️ Database)]
    D -->|Result set| X

    %% --- Regeneration Loop ---
    X -->|Error executing SQL| R[🔁 Regenerator Agent]
    R -->|Refine SQL<br/>using error feedback| A

    %% --- Summarization ---
    X -->|Successful result| S[🧠 Summarizer Agent]
    S -->|Generate NL summary| Z[💬 User Answer<br/>(Natural Language Summary)]

    %% --- Visualization ---
    S -->|Dataset| W[📊 Visualization Agent]
    W -->|Suggest & generate chart| P[🖼️ Matplotlib Chart]

    %% --- Power BI Export ---
    W -->|Optional| B[⚡ Power BI Exporter]
    B -->|Create dashboard| PB[📈 Power BI Workspace]

    %% --- Semantic Kernel & Foundry ---
    subgraph SK[Semantic Kernel / Azure Foundry]
        A
        G
        X
        R
        S
        W
        B
    end

    %% --- Styles ---
    classDef error fill=#ffdddd,stroke=#aa0000,stroke-width=1px;
    classDef service fill=#f0f7ff,stroke=#0078d4,stroke-width=1px;
    classDef data fill=#fff5cc,stroke=#c8a600,stroke-width=1px;

    note right of SK::service
        SK coordinates all agents using
        Magentic Orchestration and Azure Foundry
    end

```

```mermaid
flowchart LR
    %% --- Frontend User Interface ---
    U[🧑‍💻 User<br/>via Browser] -->|Natural language query| CL[💬 Chainlit Frontend<br/>(Python + React UI)]

    %% --- Backend API ---
    CL -->|REST / WebSocket| API[⚙️ FastAPI Backend<br/>Text-to-SQL Service]
    API -->|Configures + Routes| SK[🧠 Semantic Kernel Orchestrator]

    %% --- Multi-Agent System (Azure Foundry) ---
    subgraph AF[🏗️ Azure Foundry Agent Runtime]
        direction TB
        SK -->|Invoke| AG1[🎯 SQL Generator Agent]
        SK -->|Invoke| AG2[🛡️ Guardrail Agent]
        SK -->|Invoke| AG3[🧩 SQL Executor Agent]
        SK -->|Invoke| AG4[🔁 Regenerator Agent]
        SK -->|Invoke| AG5[🧠 Summarizer Agent]
        SK -->|Invoke| AG6[📊 Visualization Agent]
        SK -->|Invoke| AG7[⚡ Power BI Exporter]
    end

    %% --- Databases ---
    subgraph DBs[🗄️ Data Sources]
        direction TB
        DB1[(Azure SQL)]
        DB2[(BigQuery)]
        DB3[(Snowflake)]
    end

    AG3 -->|Execute SQL via adapter| DBs

    %% --- Outputs ---
    AG5 -->|Natural language summary| API
    AG6 -->|Chart image (matplotlib)| API
    AG7 -->|Power BI dashboard URL| API
    API -->|Send response (data + summary + chart)| CL

    %% --- Azure Services Integration ---
    subgraph Azure[☁️ Azure Cloud Infrastructure]
        AF
        DBs
        BI[📈 Power BI Workspace]
    end

    AG7 --> BI
```
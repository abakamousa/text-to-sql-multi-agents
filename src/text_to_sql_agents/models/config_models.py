"""
Pydantic models representing the application's hierarchical configuration.
These models are loaded by utils/config_loader.py from settings.yaml and env-specific overlays.
"""

from pydantic import BaseModel, Field
from typing import Optional


# -------------------------------------------------------------------------
# Core App Settings
# -------------------------------------------------------------------------
class AppSettings(BaseModel):
    name: str = Field("Text-to-SQL Agent", description="Name of the application.")
    environment: str = Field("development", description="Environment name: dev, staging, prod, etc.")
    log_level: str = Field("info", description="Logging level for the app.")
    port: int = Field(8000, description="Port for local or container runtime.")


# -------------------------------------------------------------------------
# Azure / Semantic Kernel / Foundry Settings
# -------------------------------------------------------------------------
class AzureSettings(BaseModel):
    openai_endpoint: Optional[str] = Field(None, description="Azure OpenAI endpoint for Semantic Kernel.")
    openai_deployment: Optional[str] = Field(None, description="Deployment name of the Azure OpenAI model.")
    use_managed_identity: bool = Field(True, description="Whether to use Managed Identity for authentication.")
    foundry_agent_name: Optional[str] = Field(None, description="Agent name to connect with Azure AI Foundry.")


# -------------------------------------------------------------------------
# Database Providers
# -------------------------------------------------------------------------
class AzureSQLSettings(BaseModel):
    server: str
    database: str
    username: str
    password: str


class BigQuerySettings(BaseModel):
    project_id: Optional[str]
    dataset: Optional[str]


class SnowflakeSettings(BaseModel):
    account: Optional[str]
    warehouse: Optional[str]
    database: Optional[str]
    schema: Optional[str]


class DatabaseSettings(BaseModel):
    provider: str = Field("azure_sql", description="Database provider: azure_sql | bigquery | snowflake")
    azure_sql: Optional[AzureSQLSettings] = None
    bigquery: Optional[BigQuerySettings] = None
    snowflake: Optional[SnowflakeSettings] = None


# -------------------------------------------------------------------------
# Orchestration and PowerBI
# -------------------------------------------------------------------------
class OrchestrationSettings(BaseModel):
    retry_max: int = Field(2, description="Maximum number of retries for SQL regeneration.")
    enable_powerbi: bool = Field(True, description="Whether to enable Power BI export integration.")


class PowerBISettings(BaseModel):
    workspace_id: Optional[str]
    dataset_name: Optional[str]
    client_id: Optional[str]
    tenant_id: Optional[str]


# -------------------------------------------------------------------------
# Root Configuration
# -------------------------------------------------------------------------
class AppConfig(BaseModel):
    app: AppSettings
    azure: AzureSettings
    database: DatabaseSettings
    orchestration: OrchestrationSettings
    powerbi: PowerBISettings

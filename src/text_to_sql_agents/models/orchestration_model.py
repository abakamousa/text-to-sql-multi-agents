# src/text_to_sql_agents/models/orchestration_models.py
from typing import Any, Dict, List, Optional
from pydantic import BaseModel


class OrchestrationStepResult(BaseModel):
    step_id: str
    agent: str
    success: bool
    output: Optional[Any] = None
    error: Optional[str] = None


class OrchestrationResult(BaseModel):
    """Final result object for orchestrated multi-agent execution."""
    status: str  # success | error
    sql_query: Optional[str] = None
    rows: Optional[List[Dict[str, Any]]] = None
    summary: Optional[str] = None
    viz_spec: Optional[Dict[str, Any]] = None
    powerbi_link: Optional[str] = None
    error: Optional[str] = None
    steps: Optional[List[OrchestrationStepResult]] = None

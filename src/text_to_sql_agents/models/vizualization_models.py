# src/text_to_sql_agents/models/visualization_models.py
from typing import Any, Dict, Optional
from pydantic import BaseModel


class VisualizationSpec(BaseModel):
    """Chart recommendation metadata for retrieved data."""
    chart_type: str
    x_field: Optional[str] = None
    y_field: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None
    config: Optional[Dict[str, Any]] = None

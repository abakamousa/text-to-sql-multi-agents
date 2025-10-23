# src/text_to_sql_agents/agents/visualization_agent.py
from typing import List, Dict, Any
from loguru import logger
from ..models.visualization_models import VisualizationSpec


class VisualizationAgent:
    """
    Agent that recommends an appropriate chart type for the returned dataset.
    """

    def __init__(self):
        logger.info("VisualizationAgent initialized.")

    async def recommend_chart(self, rows: List[Dict[str, Any]]) -> VisualizationSpec:
        """
        Analyzes result data and recommends a chart type + fields.
        """
        if not rows:
            return VisualizationSpec(
                chart_type="table",
                fields={},
                description="No data to visualize.",
                chart_data=[],
            )

        sample_row = rows[0]
        numeric_fields = [k for k, v in sample_row.items() if isinstance(v, (int, float))]
        non_numeric_fields = [k for k, v in sample_row.items() if isinstance(v, str)]

        if len(numeric_fields) >= 2:
            chart_type = "scatter"
        elif len(numeric_fields) == 1 and non_numeric_fields:
            chart_type = "bar"
        else:
            chart_type = "table"

        logger.debug(f"Recommended chart type: {chart_type}")

        return VisualizationSpec(
            chart_type=chart_type,
            fields={"x": non_numeric_fields[0] if non_numeric_fields else "index",
                    "y": numeric_fields[0] if numeric_fields else "value"},
            description=f"A {chart_type} chart is recommended based on the data fields.",
            chart_data=rows,
        )

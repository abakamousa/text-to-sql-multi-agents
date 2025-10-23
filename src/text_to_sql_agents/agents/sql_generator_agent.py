# src/text_to_sql_agents/agents/sql_generator_agent.py
from typing import Dict, Any, Optional
from loguru import logger
from ..models.sql_models import SQLQuery


class SQLGeneratorAgent:
    """
    Agent responsible for generating SQL queries from natural language input.
    """

    def __init__(self):
        # Optionally: Inject Semantic Kernel or Azure OpenAI connector
        self.model_name = "gpt-4o"
        logger.info("SQLGeneratorAgent initialized.")

    async def generate_sql(self, user_query: str, schema_snapshot: Dict[str, Any]) -> SQLQuery:
        """
        Generate an initial SQL query based on user input and schema context.
        """
        logger.debug(f"Generating SQL for query: '{user_query}'")

        # Placeholder for LLM prompt logic
        sql_text = f"-- SQL generated for query: {user_query}\nSELECT * FROM table_name LIMIT 10;"

        return SQLQuery(text=sql_text, confidence=0.8)

    async def regenerate_sql(
        self,
        user_query: str,
        schema_snapshot: Dict[str, Any],
        error_message: str,
        previous_sql: Optional[str] = None,
    ) -> SQLQuery:
        """
        Regenerate SQL after execution errors.
        Uses both the user query, schema, and prior SQL + error message for context.
        """
        logger.debug(f"Regenerating SQL due to error: {error_message}")

        # Placeholder regeneration logic
        sql_text = f"-- Regenerated SQL after error: {error_message}\nSELECT * FROM table_name;"
        return SQLQuery(text=sql_text, confidence=0.75)

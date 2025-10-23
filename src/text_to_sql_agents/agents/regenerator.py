from __future__ import annotations
from loguru import logger
from ..service.plugin_registry import PluginRegistry


class SQLRegenerator:
    """
    Agent responsible for regenerating SQL queries based on error feedback.
    """

    def __init__(self, plugin_registry: PluginRegistry, max_retries: int = 2):
        self.plugin_registry = plugin_registry
        self.max_retries = max_retries

    async def regenerate_sql(self, query: str, previous_sql: str, error_message: str):
        """
        Try to generate a corrected SQL statement when an error occurs.
        """
        logger.warning(f"Regenerating SQL due to error: {error_message}")
        attempt = 0
        sql = None

        while attempt < self.max_retries:
            attempt += 1
            logger.info(f"SQL regeneration attempt {attempt}/{self.max_retries}...")
            sql = await self.plugin_registry.invoke(
                "repair_sql",
                query=query,
                previous_sql=previous_sql,
                error=error_message,
            )
            if sql and "SELECT" in sql.upper():
                logger.success("SQL regeneration successful.")
                return sql

        logger.error("SQL regeneration failed after max retries.")
        raise RuntimeError("Unable to generate a valid SQL statement.")

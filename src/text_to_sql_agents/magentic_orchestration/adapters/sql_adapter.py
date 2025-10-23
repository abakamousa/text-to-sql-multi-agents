import asyncio
from typing import Any, Dict, List, Optional
from loguru import logger

# try to import existing project's SQLExecutor
try:
    from ...agents.executor import SQLExecutor
except Exception:
    from ...agents.executor_agent import SQLExecutor  # fallback if different naming


class SQLAdapter:
    """
    Async wrapper over the project's SQLExecutor.
    Exposes:
      - execute_query(sql) -> list[dict]
      - generate_schema_snapshot() -> dict
    """

    def __init__(self, connection_string: Optional[str] = None):
        self._conn_str = connection_string
        self._executor = SQLExecutor(connection_string) if connection_string else None

    async def execute_query(self, sql: str) -> List[Dict[str, Any]]:
        if not self._executor:
            raise RuntimeError("SQLExecutor not initialized with a connection string.")
        loop = asyncio.get_running_loop()

        def run():
            df = self._executor.execute_query(sql)
            if df is None:
                return []
            return df.to_dict(orient="records")

        return await loop.run_in_executor(None, run)

    async def generate_schema_snapshot(self) -> Dict[str, Any]:
        if not self._executor:
            return {}
        loop = asyncio.get_running_loop()

        def run():
            if hasattr(self._executor, "generate_schema_snapshot"):
                return self._executor.generate_schema_snapshot()
            return {}

        return await loop.run_in_executor(None, run)

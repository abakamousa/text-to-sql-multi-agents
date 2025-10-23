# src/text_to_sql_agents/magentic_orchestration/agent_registry.py
from typing import Any, Callable, Dict, Optional
from loguru import logger

from .adapters.semantic_kernel_adapter import SemanticKernelAdapter
from .adapters.azure_foundry_adapter import AzureFoundryAdapter
from .adapters.sql_adapter import SQLAdapter


class AgentRegistry:
    """
    Map declarative agent names used in plans to adapter functions that run them.
    """

    def __init__(
        self,
        kernel_adapter: Optional[SemanticKernelAdapter] = None,
        foundry_adapter: Optional[AzureFoundryAdapter] = None,
        sql_adapter: Optional[SQLAdapter] = None,
    ):
        self.kernel = kernel_adapter or SemanticKernelAdapter()
        self.foundry = foundry_adapter or AzureFoundryAdapter()
        self.sql = sql_adapter or SQLAdapter()

        self._mapping: Dict[str, Callable[[Dict[str, Any]], Any]] = {
            "generate_sql": self._invoke_generate_sql,
            "repair_sql": self._invoke_repair_sql,
            "summarize": self._invoke_summarize,
            "recommend_chart": self._invoke_recommend_chart,
            "guardrail_check": self._invoke_guardrail,
            "powerbi_upload": self._invoke_powerbi_upload,
            "execute_sql": self._invoke_execute_sql,
            "schema_snapshot": self._invoke_schema_snapshot,
        }

    async def invoke(self, agent_name: str, payload: Dict[str, Any]) -> Any:
        func = self._mapping.get(agent_name)
        if not func:
            raise KeyError(f"Agent '{agent_name}' is not registered.")
        logger.debug(f"AgentRegistry invoking '{agent_name}' with payload keys: {list(payload.keys())}")
        return await func(payload)

    # Semantic Kernel plugin wrappers
    async def _invoke_generate_sql(self, payload: Dict[str, Any]):
        query = payload.get("query")
        return await self.kernel.invoke_plugin("generate_sql", query=query)

    async def _invoke_repair_sql(self, payload: Dict[str, Any]):
        return await self.kernel.invoke_plugin(
            "repair_sql",
            query=payload.get("query"),
            previous_sql=payload.get("previous_sql"),
            error=payload.get("error"),
        )

    async def _invoke_summarize(self, payload: Dict[str, Any]):
        return await self.kernel.invoke_plugin("summarize", query=payload.get("query"), data=payload.get("data"))

    async def _invoke_recommend_chart(self, payload: Dict[str, Any]):
        return await self.kernel.invoke_plugin("recommend_chart", data=payload.get("data"))

    # Foundry / Tool wrappers
    async def _invoke_guardrail(self, payload: Dict[str, Any]):
        sql = payload.get("sql")
        return await self.foundry.guardrail_check(sql)

    async def _invoke_powerbi_upload(self, payload: Dict[str, Any]):
        pbix_bytes = payload.get("pbix_bytes")
        user_id = payload.get("user_id")
        return await self.foundry.upload_powerbi_report(pbix_bytes, user_id=user_id)

    # SQL adapter wrappers
    async def _invoke_execute_sql(self, payload: Dict[str, Any]):
        sql = payload.get("sql")
        return await self.sql.execute_query(sql)

    async def _invoke_schema_snapshot(self, payload: Dict[str, Any]):
        return await self.sql.generate_schema_snapshot()

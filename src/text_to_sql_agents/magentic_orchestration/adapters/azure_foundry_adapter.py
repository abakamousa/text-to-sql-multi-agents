from typing import Any, Optional
from loguru import logger

from ...service.foundry_agent_service import FoundryAgentService


class AzureFoundryAdapter:
    """
    Adapter that talks to FoundryAgentService.
    Provides:
      - guardrail_check(sql) -> bool
      - invoke_agent(prompt, context) -> Any
      - upload_powerbi_report(pbix_bytes, user_id) -> Optional[str]
    """

    def __init__(self, service: Optional[FoundryAgentService] = None):
        self.service = service
        self._started = False

    async def startup(self):
        if not self.service:
            # lazy instantiate FoundryAgentService using config loader in the service module
            raise RuntimeError("FoundryAgentService instance required")
        if not self._started:
            await self.service.initialize()
            self._started = True

    async def guardrail_check(self, sql: str) -> bool:
        await self.startup()
        try:
            # The Foundry service should expose a guardrail skill or check method
            result = await self.service.kernel.invoke_function("guardrail", "check", sql) if getattr(self.service, "kernel", None) else None
            if isinstance(result, bool):
                return result
            if isinstance(result, str) and result.lower() in ("allow", "true", "yes"):
                return True
            return False
        except Exception as e:
            logger.warning(f"Foundry guardrail check failed: {e}")
            return False

    async def invoke_agent(self, prompt: str, context: Optional[dict] = None) -> Any:
        await self.startup()
        return await self.service.invoke_agent(prompt, context=context)

    async def upload_powerbi_report(self, pbix_bytes: bytes, user_id: str) -> Optional[str]:
        await self.startup()
        try:
            return await self.service.upload_powerbi_report(pbix_bytes, user_id=user_id)
        except Exception as e:
            logger.error(f"PowerBI upload failed: {e}")
            return None

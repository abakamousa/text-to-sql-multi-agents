import asyncio
import yaml
from pathlib import Path
from typing import Any, Dict, List, Optional
from loguru import logger

from .agent_registry import AgentRegistry
from .adapters.semantic_kernel_adapter import SemanticKernelAdapter
from .adapters.azure_foundry_adapter import AzureFoundryAdapter
from .adapters.sql_adapter import SQLAdapter


class MagenticController:
    """
    Lightweight Magentic-style controller:
      - load declarative plans (YAML)
      - resolve inputs referencing previous step outputs (${step.key})
      - invoke agents via AgentRegistry
      - handle per-step retries
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
        self.registry = AgentRegistry(self.kernel, self.foundry, self.sql)
        self._plans: Dict[str, Any] = {}

    def load_plan_file(self, path: str):
        p = Path(path)
        if not p.exists():
            raise FileNotFoundError(f"Workflow plan not found: {path}")
        with p.open("r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
        self._plans = data.get("plans", {}) if isinstance(data, dict) else {}
        logger.info(f"Loaded plans from: {path}. Plans: {list(self._plans.keys())}")

    def get_plan(self, plan_name: str) -> Dict[str, Any]:
        if not self._plans:
            raise RuntimeError("No plans loaded. Call load_plan_file() first.")
        plan = self._plans.get(plan_name)
        if plan is None:
            raise KeyError(f"Plan '{plan_name}' not found.")
        return plan

    async def run_plan(self, plan_name: str, inputs: Dict[str, Any]) -> Dict[str, Any]:
        plan = self.get_plan(plan_name)
        steps: List[Dict[str, Any]] = plan.get("steps", [])
        context: Dict[str, Any] = {"inputs": inputs}
        results: Dict[str, Any] = {}

        for step in steps:
            step_id = step.get("id")
            agent_name = step.get("agent")
            raw_input = step.get("input", {})
            retries = int(step.get("retries", 0))

            resolved_input = self._resolve_input(raw_input, context)

            logger.info(f"Running step '{step_id}' -> agent '{agent_name}' (retries={retries})")
            attempt = 0
            step_result = None
            while attempt <= retries:
                attempt += 1
                try:
                    step_result = await self.registry.invoke(agent_name, resolved_input)
                    logger.info(f"Step '{step_id}' succeeded on attempt {attempt}.")
                    break
                except Exception as e:
                    logger.warning(f"Step '{step_id}' attempt {attempt} failed: {e}")
                    if attempt > retries:
                        logger.error(f"Step '{step_id}' exhausted retries and failed.")
                        raise
                    await asyncio.sleep(0.5 * attempt)

            results[step_id] = step_result
            # expose step result in context: both as value and as mapping if it's dict-like
            context[step_id] = step_result

        return {"plan": plan_name, "results": results, "context": context}

    def _resolve_input(self, raw: Any, context: Dict[str, Any]) -> Any:
        """Recursively resolve strings containing ${...} tokens against the context."""
        if isinstance(raw, dict):
            return {k: self._resolve_input(v, context) for k, v in raw.items()}
        if isinstance(raw, list):
            return [self._resolve_input(v, context) for v in raw]
        if isinstance(raw, str):
            if "${" in raw and "}" in raw:
                out = raw
                start = 0
                while True:
                    s = out.find("${", start)
                    if s == -1:
                        break
                    e = out.find("}", s)
                    if e == -1:
                        break
                    token = out[s + 2 : e]
                    try:
                        val = self._get_from_context(token, context)
                        out = out[:s] + str(val) + out[e + 1 :]
                        start = s + len(str(val))
                    except Exception:
                        # if token missing, remove placeholder
                        out = out[:s] + out[e + 1 :]
                        start = s
                return out
            return raw
        return raw

    def _get_from_context(self, token: str, context: Dict[str, Any]) -> Any:
        parts = token.split(".")
        cur = context
        for p in parts:
            if isinstance(cur, dict) and p in cur:
                cur = cur[p]
            else:
                raise KeyError(f"Context token '{token}' not found")
        return cur

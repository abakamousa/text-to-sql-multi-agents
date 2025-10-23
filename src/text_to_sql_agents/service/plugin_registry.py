# src/text_to_sql_agents/service/plugin_registry.py

from semantic_kernel import Kernel
from loguru import logger

from ..agents.sql_generator_agent import SQLGeneratorAgent
from ..agents.guardrail_agent import GuardrailAgent
from ..agents.executor_agent import SQLExecutorAgent
from ..agents.summarizer_agent import SummarizerAgent
from ..agents.visualization_agent import VisualizationAgent
from ..agents.powerbi_agent import PowerBIAgent


class PluginRegistry:
    """
    Loads all Semantic Kernel-compatible agents (as plugins)
    and registers them with the kernel runtime.
    """

    @staticmethod
    async def register_plugins(kernel: Kernel, db_adapter):
        logger.info("🔌 Registering Semantic Kernel agent plugins...")

        sql_gen = SQLGeneratorAgent()
        guardrail = GuardrailAgent()
        executor = SQLExecutorAgent(db_adapter)
        summarizer = SummarizerAgent()
        visualizer = VisualizationAgent()
        powerbi = PowerBIAgent()

        kernel.import_skill(sql_gen, skill_name="sql_generator")
        kernel.import_skill(guardrail, skill_name="guardrail")
        kernel.import_skill(executor, skill_name="executor")
        kernel.import_skill(summarizer, skill_name="summarizer")
        kernel.import_skill(visualizer, skill_name="visualization")
        kernel.import_skill(powerbi, skill_name="powerbi")

        logger.success("✅ All plugins successfully registered.")
        return kernel

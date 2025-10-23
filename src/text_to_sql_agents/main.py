# src/text_to_sql_agents/main.py

from fastapi import FastAPI, HTTPException
from loguru import logger

from src.text_to_sql_agents.utils.config_loader import get_settings
from .service.kernel_factory import KernelFactory
from .service.plugin_registry import PluginRegistry
from .service.foundry_agent_service import FoundryAgentService
from .magentic_orchestration.magentic_controller import MagenticController


# --- FastAPI initialization ---
app = FastAPI(title="Text-to-SQL Multi-Agent Backend")

# --- Load configuration ---
settings = get_settings()

# --- Global runtime objects ---
kernel = None
controller = None
foundry_service = None


@app.on_event("startup")
async def startup():
    """
    Initialize Semantic Kernel, Foundry agent, and orchestration controller
    when FastAPI application starts.
    """
    global kernel, controller, foundry_service

    logger.info(f"🚀 Starting Text-to-SQL app in {settings.app.get('environment')} mode...")

    # 1️⃣ Create Semantic Kernel
    kernel = KernelFactory.create_kernel(settings)
    plugin_registry = PluginRegistry(kernel)
    await plugin_registry.load_all_plugins()

    # 2️⃣ Initialize Azure Foundry Service
    foundry_service = FoundryAgentService(settings)
    await foundry_service.initialize()

    # 3️⃣ Initialize orchestration controller
    controller = MagenticController(kernel_adapter=None, foundry_adapter=None)
    controller.load_plan_file("src/text_to_sql_agents/magentic_orchestration/workflow_plans.yaml")

    logger.success("✅ System initialization complete — backend ready.")


@app.on_event("shutdown")
async def shutdown():
    """
    Cleanup or disconnect services on app shutdown.
    """
    logger.info("🧹 Shutting down Text-to-SQL backend...")
    if foundry_service:
        await foundry_service.shutdown()
    logger.success("✅ Clean shutdown complete.")


@app.get("/health")
async def health():
    """
    Basic health check endpoint.
    """
    return {
        "status": "ok",
        "environment": settings.app.get("environment"),
        "db_provider": settings.database.get("provider"),
        "foundry_agent": settings.azure.get("foundry_agent_name"),
    }


@app.post("/query")
async def query_endpoint(payload: dict):
    """
    Executes a full Text-to-SQL orchestration workflow.
    Expected payload:
    {
        "user_query": "Show me top 5 customers by revenue"
    }
    """
    global controller

    if not controller:
        raise HTTPException(status_code=503, detail="Controller not initialized yet")

    user_query = payload.get("user_query")
    if not user_query:
        raise HTTPException(status_code=400, detail="Missing 'user_query' field")

    logger.info(f"💬 Received user query: {user_query}")

    try:
        result = await controller.run_plan(
            plan_name="text_to_sql_basic",
            inputs={"user_query": user_query, "user_id": "api-user"},
        )
        results = result.get("results", {})
        return {
            "status": "success",
            "summary": results.get("summary"),
            "visualization": results.get("viz"),
            "sql_query": results.get("sql_query"),
            "rows": results.get("rows", []),
        }
    except Exception as e:
        logger.exception("❌ Orchestration failure.")
        raise HTTPException(status_code=500, detail=str(e))

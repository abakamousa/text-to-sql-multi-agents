# src/text_to_sql_agents/service/kernel_factory.py

from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion
from semantic_kernel.connectors.memory.azure_cognitive_search import AzureCognitiveSearchMemory
from semantic_kernel.connectors.memory.azure_blob_storage import AzureBlobStorageMemory
from loguru import logger

from ..models.config_models import AppConfig


class KernelFactory:
    """
    Factory responsible for creating and configuring a Semantic Kernel instance
    integrated with Azure OpenAI and optional memory providers.
    """

    @staticmethod
    def create_kernel(config: AppConfig) -> Kernel:
        try:
            logger.info("⚙️ Initializing Semantic Kernel...")
            kernel = Kernel()

            # --- Azure OpenAI connector ---
            if not config.azure.openai_endpoint or not config.azure.openai_deployment:
                raise ValueError("Azure OpenAI configuration is missing.")

            logger.info(f"Connecting to Azure OpenAI at {config.azure.openai_endpoint}")
            azure_openai = AzureChatCompletion(
                service_id="azure_openai",
                deployment_name=config.azure.openai_deployment,
                endpoint=config.azure.openai_endpoint,
                use_managed_identity=config.azure.use_managed_identity,
            )

            kernel.add_text_completion_service("azure_openai", azure_openai)

            # --- Optional: Azure Cognitive Search memory ---
            try:
                memory = AzureCognitiveSearchMemory()
                kernel.add_memory(memory)
                logger.debug("Azure Cognitive Search memory attached.")
            except Exception:
                logger.warning("No Azure Cognitive Search memory configured; continuing without it.")

            # --- Optional: Azure Blob memory ---
            try:
                blob_memory = AzureBlobStorageMemory()
                kernel.add_memory(blob_memory)
                logger.debug("Azure Blob memory attached.")
            except Exception:
                logger.debug("Azure Blob memory not configured; continuing.")

            logger.success("✅ Semantic Kernel initialization complete.")
            return kernel

        except Exception as e:
            logger.exception("❌ Failed to initialize Semantic Kernel.")
            raise e

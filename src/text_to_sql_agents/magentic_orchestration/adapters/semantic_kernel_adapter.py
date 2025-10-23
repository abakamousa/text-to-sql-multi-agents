
from typing import Any, Optional
from loguru import logger

from ...service.kernel_factory import KernelFactory
from ...service.plugin_registry import PluginRegistry


class SemanticKernelAdapter:
    """
    Thin adapter over KernelFactory + PluginRegistry exposing:
      - load_plugins()
      - invoke_plugin(name, **kwargs)
    """

    def __init__(self, kernel: Optional[Any] = None):
        self._kernel = kernel
        self._registry = None

    def _ensure(self):
        if self._kernel is None:
            self._kernel = KernelFactory.create_kernel(config=KernelFactory.__dict__.get("config", None)) if hasattr(KernelFactory, "create_kernel") else KernelFactory.create_kernel  # defensive
        if self._registry is None:
            self._registry = PluginRegistry(self._kernel)

    async def load_plugins(self):
        self._ensure()
        await self._registry.load_all_plugins()
        logger.info("SemanticKernelAdapter: plugins loaded.")

    async def invoke_plugin(self, name: str, **kwargs) -> Any:
        self._ensure()
        return await self._registry.invoke(name, **kwargs)

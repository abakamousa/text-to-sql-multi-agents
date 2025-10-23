import os
import yaml
from pathlib import Path
from typing import Optional
from loguru import logger

from ..models.config_models import AppConfig


def deep_merge_dict(base: dict, override: dict) -> dict:
    """Recursively merge two dictionaries."""
    result = base.copy()
    for key, value in override.items():
        if isinstance(value, dict) and key in result:
            result[key] = deep_merge_dict(result[key], value)
        else:
            result[key] = value
    return result


def load_config(env: Optional[str] = None) -> AppConfig:
    """
    Load configuration from settings.yaml, merging default and environment-specific sections.
    Environment can be specified via argument or APP_ENV environment variable.
    """
    env = env or os.getenv("APP_ENV", "development")

    config_path = Path(__file__).resolve().parents[2] / "config" / "settings.yaml"
    if not config_path.exists():
        raise FileNotFoundError(f"Configuration file not found: {config_path}")

    with open(config_path, "r") as f:
        yaml_data = yaml.safe_load(f) or {}

    base_cfg = yaml_data.get("default", {})
    env_cfg = yaml_data.get(env, {})

    merged = deep_merge_dict(base_cfg, env_cfg)

    try:
        config = AppConfig(**merged)
        logger.info(f"✅ Configuration loaded for environment: {env}")
        return config
    except Exception as e:
        logger.error(f"❌ Failed to parse configuration: {e}")
        raise

import re
from loguru import logger


class GuardrailAgent:
    """
    Agent that ensures the generated SQL is safe to execute.
    """

    def __init__(self):
        logger.info("GuardrailAgent initialized.")

    async def check_safety(self, sql_text: str) -> bool:
        """
        Returns True if the SQL statement is considered safe.
        """

        logger.debug("Running SQL safety check...")

        forbidden_patterns = [
            r"\bDROP\b",
            r"\bDELETE\b",
            r"\bUPDATE\b",
            r"\bINSERT\b",
            r"\bALTER\b",
            r"\bTRUNCATE\b",
        ]

        for pattern in forbidden_patterns:
            if re.search(pattern, sql_text, re.IGNORECASE):
                logger.warning(f"Unsafe SQL pattern detected: {pattern}")
                return False

        return True

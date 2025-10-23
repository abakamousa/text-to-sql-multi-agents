
from loguru import logger


class SummarizerAgent:
    """
    Agent that produces a natural language summary of query results.
    """

    def __init__(self):
        self.model_name = "gpt-4o"
        logger.info("SummarizerAgent initialized.")

    async def summarize_data(self, rows: list[dict]) -> str:
        """
        Generates a concise textual summary of the result set.
        """
        if not rows:
            return "No results were found for your query."

        # Simple summary logic placeholder
        sample = rows[0]
        summary = f"Your query returned {len(rows)} rows. " \
                  f"Here’s a sample record: {sample}."
        logger.debug(f"Generated summary: {summary}")
        return summary

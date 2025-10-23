from __future__ import annotations
import io
import json
import pandas as pd
import matplotlib.pyplot as plt
from loguru import logger


class PlotGenerator:
    """
    Agent that generates plots based on a chart recommendation and dataset.
    """

    def __init__(self):
        pass

    def generate_plot(self, data: pd.DataFrame, chart_recommendation: str) -> bytes:
        """
        Generate a matplotlib plot according to the recommended chart type.

        Returns:
            PNG image bytes suitable for display or export.
        """
        logger.info(f"Generating plot for chart type: {chart_recommendation}")

        fig, ax = plt.subplots(figsize=(6, 4))

        try:
            if chart_recommendation == "bar":
                data.plot(kind="bar", ax=ax)
            elif chart_recommendation == "line":
                data.plot(kind="line", ax=ax)
            elif chart_recommendation == "scatter":
                if data.shape[1] >= 2:
                    data.plot(kind="scatter", x=data.columns[0], y=data.columns[1], ax=ax)
                else:
                    logger.warning("Scatter plot requires at least two columns.")
                    data.plot(kind="line", ax=ax)
            elif chart_recommendation == "pie":
                data.sum().plot(kind="pie", ax=ax)
            elif chart_recommendation == "histogram":
                data.plot(kind="hist", ax=ax)
            else:
                data.head(10).plot(kind="bar", ax=ax)
                logger.warning(f"Unknown chart type '{chart_recommendation}', defaulting to bar chart.")

            ax.set_title(f"Visualization: {chart_recommendation}")
            plt.tight_layout()

            buffer = io.BytesIO()
            plt.savefig(buffer, format="png")
            buffer.seek(0)
            plt.close(fig)

            logger.success("Plot generated successfully.")
            return buffer.getvalue()

        except Exception as e:
            logger.error(f"Plot generation failed: {e}")
            raise

from __future__ import annotations
import pandas as pd
import sqlalchemy
from loguru import logger
from typing import Optional


class SQLExecutor:
    """
    Agent responsible for executing SQL statements against a database.
    Supports Azure SQL (default) and other backends (Snowflake, BigQuery).
    """

    def __init__(self, connection_string: str):
        self.connection_string = connection_string
        self.engine = sqlalchemy.create_engine(self.connection_string)

    def execute_query(self, sql: str) -> pd.DataFrame:
        """
        Execute a SQL query safely and return a pandas DataFrame.
        """
        logger.info(f"Executing SQL query:\n{sql}")
        try:
            df = pd.read_sql(sql, self.engine)
            logger.success(f"Query executed successfully. Rows: {len(df)}")
            return df
        except Exception as e:
            logger.error(f"SQL execution error: {e}")
            raise

    def test_connection(self) -> bool:
        """
        Verify connection to database.
        """
        try:
            with self.engine.connect() as conn:
                conn.execute(sqlalchemy.text("SELECT 1"))
            logger.success("Database connection successful.")
            return True
        except Exception as e:
            logger.error(f"Database connection failed: {e}")
            return False

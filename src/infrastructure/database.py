# standard
import sqlite3
from contextlib import contextmanager
from pathlib import Path

# framework

# user-defined
from .schema import SCHEMA_V1


class Database:
    """Manages SQLite database connection and schema."""

    def __init__(self, db_path: str):
        self.db_path = Path(db_path)
        self._connection = None

    def initialize_schema(self):
        """Initialize the database schema."""
        with self.get_connection() as conn:
            cursor = conn.cursor()

            # Create assets table
            cursor.execute(SCHEMA_V1["assets"])

            # Create excess_assets table
            cursor.execute(SCHEMA_V1["excess_assets"])

            # Create schema_versions table for future migrations
            cursor.execute(SCHEMA_V1["schema_versions"])

            # Insert initial schema version
            cursor.execute(
                """
                INSERT OR IGNORE INTO schema_versions (version, applied_at)
                VALUES (?, CURRENT_TIMESTAMP)
            """,
                ("1.0.0",),
            )

            conn.commit()

    @contextmanager
    def get_connection(self):
        """Context manager for database connections."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # Enable column access by name
        try:
            yield conn
        finally:
            conn.close()

    def execute_query(self, query: str, params: tuple = ()):
        """Execute a SELECT query and return results."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            return cursor.fetchall()

    def execute_command(self, command: str, params: tuple = ()):
        """Execute an INSERT/UPDATE/DELETE command."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(command, params)
            conn.commit()
            return cursor.rowcount

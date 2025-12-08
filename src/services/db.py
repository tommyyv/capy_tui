# standard
import sqlite3
import pathlib
from typing import List, Tuple

# framework

# user-defined


DATABASE_PATH = pathlib.Path().home() / "test.db"

class Database():
    # TODO: refactor public to non-public methods for create_table and run_query => users shouldn't be interacting with
    # these methods
    # NOTE: CRUD functions work, need to revise a few but overall, it works.
    def __init__(self, db_path=DATABASE_PATH):
        self.db_conn = sqlite3.connect(db_path)
        self.conn_cursor = self.db_conn.cursor()
        self._create_inv_table()

    def _create_inv_table(self) -> None:
        # TODO: add model field -> model TEXT NOT NULL
        query = """
            CREATE TABLE IF NOT EXISTS test_db (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                doe TEXT NOT NULL
                );
            """

        self.run_query(query)

    def add_inv_item(self, barcode: str) -> None:
        self.run_query("INSERT INTO test_db (doe) VALUES (?);", barcode)

    def fetch_item_by_id(self, doe: str) -> None:
        print(f"getting item by {doe}: ", self.conn_cursor.execute(
            "SELECT * FROM test_db WHERE doe = ?", (doe,)).fetchone())

    # [(int, str)] => [(id, doe), (id, doe),...]
    def fetch_all_items(self) -> List[Tuple[int, str]]:
        query = "SELECT * FROM test_db;"
        return self.run_query(query).fetchall()

    # TODO: fix functionality...should update the entry's doe, model, etc...where doe = MATCH
    def update_item(self, doe: str) -> None:
        self.conn_cursor.execute(
            "UPDATE test_db SET name = ? WHERE doe = ?", ('new device 3', doe))

        self.conn.commit()

    def delete_item(self, doe: str) -> None:
        self.run_query("DELETE FROM test_db WHERE doe = ?;", doe)

    def clear_db(self):
        self.run_query("DELETE FROM test_db;")

    def run_query(self, query, *query_args):
        result = self.conn_cursor.execute(query, query_args)
        self.db_conn.commit()
        return result

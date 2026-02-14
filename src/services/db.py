# standard
import sqlite3
import pathlib
import csv
from typing import List, Tuple

# framework

# user-defined


DATABASE_PATH = pathlib.Path().home() / "test.db"


class Database:
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
                doe TEXT NOT NULL,
                mac_address TEXT NOT NULL
                );
            """

        self.run_query(query)

    def add_inv_item(self, barcode: str, mac_address: str) -> None:
        self.run_query(
            "INSERT INTO test_db (doe, mac_address) VALUES (?, ?);",
            barcode,
            mac_address,
        )

    # TOOD(bug): logic error potentially here for the search box
    def fetch_item_by_id(self, doe: str) -> List[Tuple[int, str]]:
        print(f"fetching item by doe: {doe}")
        return self.run_query("SELECT * from test_db WHERE doe = ?;", doe).fetchall()

    # [(int, str)] => [(id, doe), (id, doe),...]
    def fetch_all_items(self) -> List[Tuple[int, str]]:
        query = "SELECT * FROM test_db;"
        return self.run_query(query).fetchall()

    # TODO: fix functionality...should update the entry's doe, model, etc...where doe = MATCH
    def update_item(self, doe: str) -> None:
        self.run_query("UPDATE test_db SET name = ? WHERE doe = ?;", doe)
        # self.conn_cursor.execute(
        #     "UPDATE test_db SET name = ? WHERE doe = ?", ("new device 3", doe)
        # )

    def delete_item(self, doe: str) -> None:
        self.run_query("DELETE FROM test_db WHERE doe = ?;", doe)

    def clear_db(self):
        self.run_query("DELETE FROM test_db;")

    def export_to_csv(self):
        """
        1. connect to db, if havent already (done)
        2. grab headers (eh)
        3. fetch rows (eh)
        4. write to csv (eh)
        5. save csv file with current timestamp (not done)
        6. close connection (eh)
        """
        # conn already done

        # header rows
        # NOTE: this works...now i need to fix the saved path
        project_root = pathlib.Path(__file__).resolve().parent.parent

        with open(
            f"{project_root}/data/data.csv", "w", newline="", encoding="utf-8"
        ) as f:
            writer = csv.writer(f)

            # Write column headers
            writer.writerow(
                [description[0] for description in self.conn_cursor.description]
            )

            # Write data rows
            writer.writerows(self.fetch_all_items())

        # NOTE: what file am i accessing???
        # csv_file should be a directory path => how would i make the csv create a new file everytime with the correct
        # timestamp?

    def backup_db(src_path: str, dst_path: str):
        pass

    def run_query(self, query, *query_args):
        result = self.conn_cursor.execute(query, query_args)
        self.db_conn.commit()
        return result

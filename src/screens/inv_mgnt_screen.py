# standard
from typing import List, Tuple

# framework
from textual.widgets import DataTable

# user-defined
from services.db import Database
from screens.base_screen import BaseScreen
from components.barcode_input_widget import BarcodeInputWidget


class InvMgntScreen(BaseScreen):
    db: Database
    table: DataTable

    def __init__(self, db: Database) -> None:
        super().__init__()
        self.db = db

    def on_mount(self) -> None:
        content = self.query_one("#content")

        self.table = DataTable()

        content.mount(self.table)
        content.mount(BarcodeInputWidget(self.db, self.refresh_table))

        self.refresh_table()

    def refresh_table(self) -> None:
        self.table.clear(columns=True)

        rows: List[Tuple[int, str]] = self.db.fetch_all_items()

        self.table.add_column("ID")
        self.table.add_column("DOE")

        for row in rows:
            self.table.add_row(str(row[0]), row[1])

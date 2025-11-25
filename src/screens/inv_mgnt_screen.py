# standard
from typing import List, Tuple

# framework
from textual.app import ComposeResult
from textual.containers import Vertical
from textual.screen import Screen
from textual.widgets import DataTable

# user-defined
from services.db import Database
from widgets.barcode_input_widget import BarcodeInputWidget


class InvMgntScreen(Screen):
    db: Database
    table: DataTable

    def __init__(self, db: Database) -> None:
        super().__init__()
        self.db = db

    def compose(self) -> ComposeResult:
        yield Vertical(
            DataTable(id="inv_table"),
            BarcodeInputWidget(self.db, self.refresh_table)
        )

    def on_mount(self) -> None:
        self.table = self.query_one("#inv_table", DataTable)

        # self.table = DataTable()

        # content.mount(self.table)
        # content.mount(BarcodeInputWidget(self.db, self.refresh_table))

        self.refresh_table()

    def refresh_table(self) -> None:
        self.table.clear(columns=True)

        rows: List[Tuple[int, str]] = self.db.fetch_all_items()

        self.table.add_column("ID")
        self.table.add_column("DOE")

        for row in rows:
            self.table.add_row(str(row[0]), row[1])

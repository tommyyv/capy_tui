from typing import List, Tuple
from textual.app import ComposeResult
from textual.containers import Horizontal
from textual.widget import Widget
from textual.widgets import DataTable
from textual import on

from widgets.util_widget_test import UtilBoxWidget


class DatabaseWidget(Widget):
    # DEFAULT_CSS = """
    #
    # Screen {
    #     layout: vertical;
    # }
    #
    # /* --- MAIN GRID LAYOUT --- */
    # #main-grid {
    #     layout: grid;
    #     grid-size: 2;
    #     grid-columns: 2fr 1fr;
    #     height: 100%;
    # }
    #
    # /* --- TABLE SIDE (2/3) --- */
    # #inv_table {
    #     height: 100%;
    #     border: round $accent;
    #     padding: 1 2;
    # }
    #
    # /* --- UTIL SIDE (1/3) --- */
    # #util-box {
    #     border: round $secondary;
    #     background: $surface;
    #     padding: 1 2;
    #     height: 100%;
    # }
    #
    # /* --- UTIL BOX INTERNAL SPACING --- */
    # #utilbox-container {
    #     layout: vertical;
    #     height: 100%;
    # }
    #
    # /* Inputs spacing */
    # Input {
    #     margin-bottom: 1;
    # }
    #
    # /* Buttons spacing */
    # Button {
    #     margin-top: 1;
    #     width: 100%;
    # }
    #
    # /* Optional: stronger visual identity */
    # #util-box Label {
    #     text-style: bold;
    #     margin-bottom: 1;
    # }
    # """
    def __init__(self, db):
        super().__init__()
        self.db = db

    def compose(self) -> ComposeResult:
        with Horizontal():
            yield DataTable(id="inv_table")
            yield UtilBoxWidget()

    def on_mount(self) -> None:
        self.table = self.query_one("#inv_table", DataTable)
        self.table.add_columns("ID", "DOE", "MAC_ADDRESS")
        self.refresh_all_items()

    # ----------------------
    # Centralized Rendering
    # ----------------------

    def refresh_table(self, rows: List[Tuple[int, str, str]]) -> None:
        self.table.clear()
        for row in rows:
            self.table.add_row(str(row[0]), row[1], row[2])

    def refresh_all_items(self) -> None:
        rows = self.db.fetch_all_items()
        self.refresh_table(rows)

    # ----------------------
    # Intent Handlers
    # ----------------------

    @on(UtilBoxWidget.AddItem)
    def handle_add(self, message: UtilBoxWidget.AddItem) -> None:
        self.db.add_inv_item(message.barcode, message.mac)
        self.refresh_all_items()

    @on(UtilBoxWidget.DeleteItem)
    def handle_delete(self, message: UtilBoxWidget.DeleteItem) -> None:
        self.db.delete_item(message.item_id)
        self.refresh_all_items()

    @on(UtilBoxWidget.ClearDatabase)
    def handle_clear(self) -> None:
        self.db.clear_db()
        self.refresh_all_items()

    @on(UtilBoxWidget.SearchItem)
    def handle_search(self, message: UtilBoxWidget.SearchItem) -> None:
        rows = self.db.fetch_item_by_id(message.item_id)
        if rows:
            self.refresh_table(rows)

    @on(UtilBoxWidget.ExportData)
    def handle_export(self) -> None:
        self.db.export_to_csv()

    @on(UtilBoxWidget.ImportData)
    def handle_import(self) -> None:
        self.db.import_from_csv()

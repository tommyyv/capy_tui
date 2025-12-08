# standard
from typing import List, Tuple

# framework
from textual import on
from textual.app import ComposeResult
from textual.containers import Container
from textual.widget import Widget
from textual.widgets import DataTable, Input, Button, Label


# user-defined


# pseudo code
# create a database object => pass a Database object into this widget from the main screen
# the widget composition is a datatable of the database
# upon mounting this widget, i want the latest instance of the datatable
# every time a change happens or an event, refresh the datatable of the database

class TestDatabaseWidget(Widget):
    DEFAULT_CSS = """
        #db-container {
            background: green;
        }

    """

    def __init__(self, db):
        super().__init__()
        self.db = db

    def compose(self) -> ComposeResult:
        with Container(id="db-container"):
            table = DataTable(id="inv_table")
            yield table
            yield Label("TEST LABEL 1: ")
            yield Input(id="barcode", placeholder="enter item...")
            yield Button("ADD", id="add")

    def on_mount(self) -> None:
        self.table = self.query_one("#inv_table", DataTable)
        self.refresh_table_callback()

    def refresh_table_callback(self) -> None:
        self.table.clear(columns=True)

        rows: List[Tuple[int, str]] = self.db.fetch_all_items()

        self.table.add_column("ID")
        self.table.add_column("DOE")

        for row in rows:
            self.table.add_row(str(row[0]), row[1])

    @on(Input.Submitted)
    @on(Button.Pressed)
    def on_input_submitted(self) -> None:
        input: str = self.query_one(Input)
        barcode: str = input.value

        # TODO: input validation
        # TODO(bug): guard clause for existing

        if barcode:
            self.db.add_inv_item(barcode)
            input.value = ""
            self.refresh_table_callback()

    async def on_db_refresh(self) -> None:
        pass

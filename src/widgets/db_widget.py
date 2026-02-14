# standard
from typing import List, Tuple

# framework
from textual import on
from textual.app import ComposeResult
from textual.containers import Container
from textual.widget import Widget
from textual.widgets import DataTable, Input, Button, Label


# user-defined


class DatabaseWidget(Widget):
    # DEFAULT_CSS = """
    #     #db-container {
    #         background: green;
    #     }
    #
    # """

    def __init__(self, db):
        super().__init__()
        self.db = db

    def compose(self) -> ComposeResult:
        with Container(id="db-container"):
            table = DataTable(id="inv_table")
            yield table
            yield Input(id="barcode", placeholder="enter item...")
            yield Input(id="mac", placeholder="enter mac address")
            yield Button("ADD", id="add")
            yield Button("DELETE ID", id="delete_id")
            yield Button("CLEAR DATABASE", id="clear")
            yield Button("SEARCH ITEM", id="search")
            yield Button("EXPORT", id="export")

    def on_mount(self) -> None:
        self.table = self.query_one("#inv_table", DataTable)
        self.refresh_all_items()

    def refresh_table_callback(self, rows: List[Tuple[int, str, str]]) -> None:
        self.table.clear(columns=True)

        # rows: List[Tuple[int, str]] = self.db.fetch_all_items()

        self.table.add_column("ID")
        self.table.add_column("DOE")
        self.table.add_column("MAC_ADDRESS")

        for row in rows:
            self.table.add_row(str(row[0]), row[1], row[2])

    def refresh_all_items(self) -> None:
        rows = self.db.fetch_all_items()
        self.refresh_table_callback(rows)

    @on(Input.Submitted, "#add")
    @on(Button.Pressed, "#add")
    def on_input_submitted(self) -> None:
        input: str = self.query_one(Input)
        mac_input: str = self.query_one("#mac", Input)
        barcode: str = input.value[5:]
        mac_address: str = mac_input.value

        # TODO: add input validation
        # TODO(bug): guard clause for existing

        if barcode and mac_address:
            self.db.add_inv_item(barcode, mac_address)
            input.value = ""
            self.refresh_all_items()

    @on(Button.Pressed, "#delete_id")
    def on_cancel_button_event(self) -> None:
        input: str = self.query_one(Input)
        id: str = input.value

        if id:
            self.db.delete_item(id)
            input.value = ""
            self.refresh_all_items()

    @on(Button.Pressed, "#clear")
    def on_clear_button_event(self) -> None:
        self.db.clear_db()
        self.refresh_all_items()

    @on(Button.Pressed, "#search")
    def on_search_button_pressed(self) -> None:
        input: str = self.query_one(Input)
        item_id: str = input.value

        print("item id before validation: ", item_id)

        if item_id:
            print("item id within validation: ", item_id)
            print("executing db operation command...")
            # TODO(bug): fix fetched data => this is where the bug is and it returns None
            rows = self.db.fetch_item_by_id(item_id)
            print("this is what rows is fetched by item id: ", rows)

            # TODO(bug): fix how the database returns the results. they aren't exact matches even if the search box is.
            # the search query displays the same wrong result even if the input is wrong (not an entry)

            print("rows from search function", rows)
            self.refresh_table_callback(rows)

    @on(Button.Pressed, "#export")
    def on_export_csv(self) -> None:
        print("[TEST] export to csv [TEST]")
        self.db.export_to_csv()

    async def on_db_refresh(self) -> None:
        pass

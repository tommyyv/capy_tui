from typing import List, Tuple
from textual.widget import Widget
from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical, VerticalScroll
from textual import on

from textual.widgets import (
    DataTable,
    Input,
    Button,
)

# import screens.home


class DatabaseWidget(Widget):
    DEFAULT_CSS = """
        #db-container {
            background: gray;
        }

    """

    def __init__(self, db):
        super().__init__()
        self.db = db

    def compose(self) -> ComposeResult:
        with Horizontal(id="db-container"):
            table = DataTable(id="inv_table")
            with VerticalScroll(id="dataview", classes="with-border"):
                yield table
            with Vertical(id="utility-controls", classes="with-border"):
                yield Input(id="barcode", placeholder="enter item...")
                yield Input(id="mac", placeholder="enter mac address")
                yield Button("ADD", id="add")
                yield Button("DELETE ID", id="delete_id")
                yield Button("CLEAR DATABASE", id="clear")
                yield Button("SEARCH ITEM", id="search")
                yield Button("EXPORT", id="export")
                yield Button("REFRESH", id="refresh")
                yield Button("GO BACK", id="go_back")

    def on_mount(self) -> None:
        self.table = self.query_one("#inv_table", DataTable)
        self.refresh_all_items()

    def refresh_table_callback(self, rows: List[Tuple[int, str, str]]) -> None:
        self.table.clear(columns=True)

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
        input_widget: Input = self.query_one(Input)
        mac_input: Input = self.query_one("#mac", Input)
        barcode: str = input_widget.value[5:]
        mac_address: str = mac_input.value

        if barcode and mac_address:
            self.db.add_inv_item(barcode, mac_address)
            input_widget.value = ""
            self.refresh_all_items()

    @on(Button.Pressed, "#delete_id")
    def on_cancel_button_event(self) -> None:
        input_widget: Input = self.query_one(Input)
        id: str = input_widget.value

        if id:
            self.db.delete_item(id)
            input_widget.value = ""
            self.refresh_all_items()

    @on(Button.Pressed, "#clear")
    def on_clear_button_event(self) -> None:
        self.db.clear_db()
        self.refresh_all_items()

    @on(Button.Pressed, "#search")
    def on_search_button_pressed(self) -> None:
        input_widget: Input = self.query_one(Input)
        item_id: str = input_widget.value
        if item_id:
            rows = self.db.fetch_item_by_id(item_id)

            self.refresh_table_callback(rows)

    @on(Button.Pressed, "#export")
    def on_export_csv(self) -> None:
        print("[TEST] export to csv [TEST]")
        self.db.export_to_csv()

    @on(Button.Pressed, "#refresh")
    def on_refresh(self) -> None:
        self.refresh_all_items()

    # @on(Button.Pressed, "#go_back")
    # def on_back_button_pressed(self) -> None:
    #     self.app.switch_screen(screens.home.Home())

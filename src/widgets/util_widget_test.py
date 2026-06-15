from textual.app import ComposeResult
from textual.containers import Container, Horizontal, Vertical
from textual.widget import Widget
from textual.widgets import Input, Label, Button
from textual.message import Message
from textual import on


class UtilBoxWidget(Widget):
    class AddItem(Message):
        def __init__(self, barcode: str, mac: str) -> None:
            self.barcode = barcode
            self.mac = mac
            super().__init__()

    class DeleteItem(Message):
        def __init__(self, item_id: str) -> None:
            self.item_id = item_id
            super().__init__()

    class ClearDatabase(Message):
        pass

    class SearchItem(Message):
        def __init__(self, item_id: str) -> None:
            self.item_id = item_id
            super().__init__()

    class ExportData(Message):
        pass

    class ImportData(Message):
        pass

    def compose(self) -> ComposeResult:
        with Vertical(id="utilbox-container"):
            yield Label("Database Controls")

            yield Input(id="barcode", placeholder="Enter barcode")
            yield Input(id="mac", placeholder="Enter MAC address")
            yield Input(id="item_id", placeholder="Enter ID for delete/search")

            yield Label("LALA")
            yield Button("ADD", id="add")
            yield Button("DELETE BY ID", id="delete_id")
            yield Button("SEARCH ITEM", id="search")
            yield Button("EXPORT", id="export")
            yield Button("CLEAR DATABASE", id="clear")

    # ----------------------
    # Event → Intent Messages
    # ----------------------

    @on(Button.Pressed, "#add")
    def handle_add(self) -> None:
        barcode = self.query_one("#barcode", Input).value
        mac = self.query_one("#mac", Input).value

        if barcode and mac:
            self.post_message(self.AddItem(barcode, mac))
            self.query_one("#barcode", Input).value = ""
            self.query_one("#mac", Input).value = ""

    @on(Button.Pressed, "#delete_id")
    def handle_delete(self) -> None:
        item_id = self.query_one("#item_id", Input).value
        if item_id:
            self.post_message(self.DeleteItem(item_id))
            self.query_one("#item_id", Input).value = ""

    @on(Button.Pressed, "#clear")
    def handle_clear(self) -> None:
        self.post_message(self.ClearDatabase())

    @on(Button.Pressed, "#search")
    def handle_search(self) -> None:
        item_id = self.query_one("#item_id", Input).value
        if item_id:
            self.post_message(self.SearchItem(item_id))

    @on(Button.Pressed, "#export")
    def handle_export(self) -> None:
        self.post_message(self.ExportData())

    @on(Button.Pressed, "#import")
    def handle_export(self) -> None:
        self.post_message(self.ImportData())

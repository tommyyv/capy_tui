# standard

# framework
from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical
from textual.widgets import (
    Input,
    Button,
    Label
)
from textual import on

# user-defined
from services.db import Database


class BarcodeInputWidget(Horizontal):
    db: Database

    def __init__(self, db: Database, refresh_callback):
        super().__init__()
        self.db = db
        self.refresh_callback = refresh_callback

    def compose(self) -> ComposeResult:
        yield Vertical(
            Input(placeholder="Enter item"),
            Button("Submit")
        )

    @on(Input.Submitted)
    @on(Button.Pressed)
    def on_input_submitted(self, db: Database) -> None:
        input: str = self.query_one(Input)
        barcode: str = input.value

        # TODO: input validation
        # TODO(bug): guard clause for existing

        if barcode:
            self.db.add_inv_item(barcode)
            input.value = ""
            self.refresh_callback()

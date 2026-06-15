# standard

# framework
from textual.app import ComposeResult
from textual.containers import Grid
from textual.screen import Screen
from textual.widgets import (
    Button,
    Label
)
from textual import on

# user-defined


class Quit(Screen):
    def compose(self) -> ComposeResult:
        with Grid():
            yield Label("Are you sure you want to quit?")
            yield Button("YES", id="yes", variant="success")
            yield Button("NO", id="no", variant="error")

    @on(Button.Pressed, "#yes")
    def action_handle_yes(self):
        self.dismiss(True)

    @on(Button.Pressed, "#no")
    def action_handlen_no(self):
        self.dismiss(False)

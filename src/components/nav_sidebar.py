# standard

# framework
from textual.app import ComposeResult
from textual.containers import Vertical
from textual.widgets import Button

# user-defined


class NavSidebar(Vertical):
    def compose(self) -> ComposeResult:
        yield Button("Inventory", id="inv-mgnt")
        yield Button("Placeholder")
        yield Button("Placeholder")
        yield Button("Placeholder")

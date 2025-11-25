# standard

# framework
from textual.app import ComposeResult
from textual.containers import HorizontalGroup, Vertical, Horizontal, Container
from textual.widget import Widget
from textual.widgets import (
    Button,
    Static,
)


# user-defined
class HomeNavContainer(Container):
    DEFAULT_CSS = """
    HomeNavContainer {
        background: $panel;
        border: round $primary;
    }

    .container {
        border: heavy red;
    }
    """

    def compose(self) -> ComposeResult:
        with Container(classes="container"):
            with Horizontal(classes="row"):
                with Vertical(classes="column"):
                    yield Button("Inventory")
                    yield Button("Reports")
                with Vertical(classes="column"):
                    yield Button("Excess")
                    yield Button("Quit")

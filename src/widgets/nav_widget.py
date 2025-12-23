# standard

# framework
from textual.app import ComposeResult
from textual.containers import Container
from textual.widget import Widget
from textual.widgets import Button

# user-defined


class NavBoxWidget(Widget):
    DEFAULT_CSS = """
        #nav-btn-container {
            layout: grid;
            grid-size: 2;
            align: center middle;
        }

    """

    def compose(self) -> ComposeResult:
        with Container(id="nav-btn-container"):
            yield Button("1")
            yield Button("2")
            yield Button("3")
            yield Button("4")
            yield Button("5")

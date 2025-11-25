# standard

# framework
from textual.app import ComposeResult
from textual.containers import Container
from textual.widget import Widget
from textual.widgets import Static


# user-defined


class TestDatabaseWidget(Widget):
    DEFAULT_CSS = """
        #db-container {
            background: green;
        }

    """

    def compose(self) -> ComposeResult:
        with Container(id="db-container"):
            yield Static("DATABASE")

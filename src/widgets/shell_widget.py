# standard

# framework
from textual.app import ComposeResult
from textual.containers import (
    Grid,
    Container,
)
from textual.widget import Widget
from textual.widgets import (
    Header,
    Footer
)

# user-defined
from widgets.nav_sidebar import NavSidebar


class Shell(Grid):
    def compose(self) -> ComposeResult:
        yield Header()
        yield Container(id="content")
        yield Footer()

# standard

# framework
from textual.app import ComposeResult
from textual.screen import Screen
from textual.containers import (
    Container,
    Horizontal
)
from textual.widgets import (
    Header,
    Footer,
    Button,
)
from textual import on

# user-defined
from components.nav_sidebar import NavSidebar


class BaseScreen(Screen):
    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        yield Horizontal(
            NavSidebar(id="nav_sidebar"),
            Container(id="content")
        )
        yield Footer()

    @on(Button.Pressed)
    def on_button_pressed(self):
        pass

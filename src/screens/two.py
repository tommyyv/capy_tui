from textual.screen import Screen
from textual.app import ComposeResult
from textual.widgets import Header, Footer, Placeholder, Button
from textual import on

import home


class Box(Placeholder):
    pass


class Two(Screen):
    def compose(self) -> ComposeResult:
        yield Header()
        yield Button(id="go_back")
        yield Footer(id="footer")

    @on(Button.Pressed, "#go_back")
    def on_go_back_button_pressed(self) -> None:
        self.app.switch_screen(home.Home())

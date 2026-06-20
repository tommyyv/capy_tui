# standard
# framework

from textual import on
from textual.app import App, ComposeResult
from textual.containers import Center
from textual.screen import Screen
from textual.widgets import Button, Header

# user-defined
import one
import two


class Home(Screen):
    DEFAULT_CSS = """
        Screen {
            align: center middle;
        }

        Button{
            width: 50;
            height: 5;
            margin: 2;
            padding: 1;
        }
    """

    def compose(self) -> ComposeResult:
        with Center():
            yield Header(show_clock=True)
            yield Button("SCAN", id="scan", classes="with-border")
            yield Button("EXCESS", id="excess", classes="with-border")
            yield Button("REPORTS", id="reports", classes="with-border")
            yield Button("DOCS", id="docs", classes="with-border")

    @on(Button.Pressed, "#scan")
    def on_scan_button_pressed(self) -> None:
        self.app.switch_screen(one.One())

    @on(Button.Pressed, "#excess")
    def on_excess_button_pressed(self) -> None:
        self.app.switch_screen(two.Two())


class Layout(App):
    CSS = """
    .with-border {
        border: heavy green;
    }
    """

    TITLE = "CapyTUI"

    def on_mount(self) -> None:
        self.theme = "gruvbox"
        self.push_screen(Home())


if __name__ == "__main__":
    app = Layout()
    app.run()

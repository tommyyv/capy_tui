# standard
# framework

from textual import on
from textual.app import ComposeResult
from textual.containers import Center
from textual.screen import Screen
from textual.widgets import Button, Header

# user-defined
from screens.scan import Scan

# from screens.excess import Excess
# from screens.reports import Reports
from services.db import Database

one_table = "scan_table"
two_table = "excess_table"
three_table = "test_db"


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

    def __init__(self, db: Database) -> None:
        super().__init__()
        self.db = db

    def compose(self) -> ComposeResult:
        with Center():
            yield Header(show_clock=True)
            yield Button("SCAN", id="scan", classes="with-border")
            yield Button("EXCESS", id="excess", classes="with-border")
            yield Button("REPORTS", id="reports", classes="with-border")
            yield Button("DOCS", id="docs", classes="with-border")

    @on(Button.Pressed, "#scan")
    def on_scan_button_pressed(self) -> None:
        self.app.switch_screen(Scan(self.db))

    # @on(Button.Pressed, "#excess")
    # def on_excess_button_pressed(self) -> None:
    #     self.app.switch_screen(Excess())
    #
    # @on(Button.Pressed, "#reports")
    # def on_reports_button_pressed(self) -> None:
    #     self.app.switch_screen(Reports())

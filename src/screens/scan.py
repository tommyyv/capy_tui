# standard
# framework
from textual.app import ComposeResult
from textual.containers import (
    Horizontal,
)
from textual.screen import Screen

# user-defined
from widgets.db_widget import DatabaseWidget
from services.db import Database


class Scan(Screen):
    DEFAULT_CSS = """
        #dataview {
            width: 2fr
        }

        #utility-controls {
            width: 1fr
        }

    """

    def __init__(self, db: Database) -> None:
        super().__init__()
        self.db = db

    def compose(self) -> ComposeResult:
        with Horizontal():
            yield DatabaseWidget(self.db)

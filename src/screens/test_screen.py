# standard

# framework
from textual.app import ComposeResult
from textual.screen import Screen
from textual.containers import Container, Vertical
from textual.widgets import Static, Header, Footer

# user-defined
from widgets.test_nav_widget import TestNavBoxWidget
from widgets.test_util_widget import TestUtilBoxWidget
from widgets.test_db_widget import TestDatabaseWidget
from services.db import Database


class TestScreen(Screen):
    DEFAULT_CSS = """
        #screen-grid {
            layout: grid;
            grid-size: 3;
            grid-columns: 1fr;
            grid-gutter: 1;
        }

        #left-pane {
            background: blue;
            column-span: 2;
        }
        #right-pane {
            layout: grid;
            grid-size: 1 3;
            grid-rows: 1fr;
            background: black;
        }

        #top-right-pane {
            background: gray;
            height: 75%;
            row-span: 2;
        }

        #bottom-right-pane {
            background: purple;
            height: 100%;
        }

    """

    def compose(self) -> ComposeResult:
        # TODO: remove extra stuff
        # TODO: add header contents
        # TODO: add footer contents

        yield Header()
        with Container(id="screen-grid"):
            with Container(id="left-pane"):
                yield Static("DATABASE (del)")
                yield TestDatabaseWidget(db=Database())
            with Vertical(id="right-pane"):
                with Container(id="top-right-pane"):
                    yield Static("UTIL BOX (del)")
                    yield TestUtilBoxWidget()
                with Container(id="bottom-right-pane"):
                    yield Static("NAVBOX (del)")
                    yield TestNavBoxWidget()
        yield Footer()

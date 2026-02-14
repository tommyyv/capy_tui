# standard

# framework
from textual.app import ComposeResult
from textual.screen import Screen
from textual.containers import Container, Vertical
from textual.widgets import Static, Header, Footer

# user-defined
from widgets.nav_widget import NavBoxWidget
from widgets.util_widget import UtilBoxWidget
from widgets.db_widget import DatabaseWidget
from services.db import Database


class HomeScreen(Screen):
    DEFAULT_CSS = """
        #screen-grid {
            layout: grid;
            grid-size: 3;
            grid-columns: 1fr;
            grid-gutter: 1;
        }

        #left-pane {
            column-span: 2;
        }
        #right-pane {
            layout: grid;
            grid-size: 1 3;
            grid-rows: 1fr;
        }

        #top-right-pane {
            height: 75%;
            row-span: 2;
        }

        #bottom-right-pane {
            height: 100%;
        }

    """

    def compose(self) -> ComposeResult:
        # TODO: remove extra stuff
        # TODO: add header contents
        # TODO: add footer contents

        yield Header(show_clock=True)
        with Container(id="screen-grid"):
            with Container(id="left-pane"):
                yield DatabaseWidget(db=Database())
            with Vertical(id="right-pane"):
                with Container(id="top-right-pane"):
                    yield Static("UTIL BOX (del)")
                    yield UtilBoxWidget()
                with Container(id="bottom-right-pane"):
                    yield Static("NAVBOX (del)")
                    yield NavBoxWidget()
        yield Footer()

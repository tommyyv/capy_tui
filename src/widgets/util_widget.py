from textual.app import ComposeResult
from textual.containers import Container, Horizontal
from textual.widget import Widget
from textual.widgets import Input, Label, Button


class UtilBoxWidget(Widget):
    DEFAULT_CSS = """
        #utilbox-container {
            layout: grid;
            grid-size: 1 3;
            grid-rows: 1fr;
        }

        #top-pane {
            row-span: 2;
        }
        #bottom-pane {
            row-span: 1;
            align-horizontal: center;
        }

    """

    def compose(self) -> ComposeResult:
        with Container(id="utilbox-container"):
            with Container(id="top-pane"):
                with Horizontal():
                    yield Label("TEST LABEL 1: ")
                    yield Input(placeholder="input...")
                with Horizontal():
                    yield Label("TEST LABEL 2: ")
                    yield Input(placeholder="input...")
                with Horizontal():
                    yield Label("TEST LABEL 3: ")
                    yield Input(placeholder="input...")
            with Horizontal(id="bottom-pane"):
                yield Button("ADD", id="add")
                yield Button("DELETE BY ID", id="delete_id")
                yield Button("EXPORT", id="export")
                yield Button("CLEAR DATABASE", id="clear")

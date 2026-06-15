from textual.app import ComposeResult
from textual.containers import Container, Horizontal
from textual.widget import Widget
from textual.widgets import Input, Label, Button
from textual.message import Message


# TODO: move over operations from database widget
# TODO: create sub-classes (read, add, delete, update)
# TODO: add event handlers (read, add, delete, update)


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

    # TODO: add add event handler
    class AddItem(Message):
        def __init__(self, barcode: str, mac: str) -> None:
            self.barcode = barcode
            self.mac = mac
            super().__init__()

    # TODO: add search event handler
    class SearchItem(Message):
        def __init__(self, barcode: str) -> None:
            self.barcode = barcode
            super().__init__()

    # TODO: add delete event handler
    class DeleteItem(Message):
        def __init__(self, barcode: str) -> None:
            self.barcode = barcode
            super().__init__()

    class ClearDatabase(Message):
        def __init__(self) -> None:
            super().__init__()

    class ExportData(Message):
        def __init__(self) -> None:
            super().__init__()

    class ImportData(Message):
        def __init__(self) -> None:
            super().__init__()

    def compose(self) -> ComposeResult:
        # TODO: update ui
        # DESIGN: Container
        # DESIGN: Label
        # DESIGN: Input Box (input fields)
        # DESIGN: Button Box (button fields)
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

    # this widget should be getting access to the database service. it has know what the state is and
    # how it's getting db operations from
    # so how would the db_widget get the latest datatable?? should it just be render?
    # the database widget should just be on_mount and get refresh the data. what about refresh after
    # each db operation?

    # event handlers -> intent messages

    def handle_add():
        pass

    def handle_delete():
        pass

    def handle_search():
        pass

    def handle_clear():
        pass

    def handle_export():
        pass

    def handle_import():
        pass

# standard

# framework
from textual.app import App, ComposeResult
from textual.widgets import (
    Footer,
    Header,
)

from screens.home_screen import HomeScreen
from screens.test_screen import TestScreen

# user-defined
from services.db import Database

'''data model
id: PK
name: String
model: String
barcode: String
quantity: Integer
initial_entry: DateTime
last_updated: DateTime
'''
########

# MAIN #
########


# NOTE: work outside in
# DESIGN: screen(container) -> container layout(horiz, vert, etc)-> components(widgets) -> behavior/functionality
# DESIGN: think about functionality/behavior of that screen and work out, what needs to be on the screen to make the
# functionality work
# NOTE: container is similar to astros base layout and page specific content
class CapyTUI(App):
    TITLE = "CapyTUI"
    # CSS_PATH = "styles/main.tcss"
    BINDINGS = []
    SCREENS = {
        "home": HomeScreen,
        "test": TestScreen
    }
    INITIAL_SCREEN = "home"
    db: Database

    def __init__(self):
        super().__init__()
        self.db = Database()

    def compose(self) -> ComposeResult:
        # yield Shell()
        yield Header()
        yield Footer()

    def on_mount(self) -> None:
        self.theme = "gruvbox"
        self.push_screen("test")


if __name__ == "__main__":
    CapyTUI().run()

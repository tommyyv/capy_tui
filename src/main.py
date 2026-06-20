# standard

# framework
from textual.app import App

# user-defined
from screens.home import Home

"""data model
id: PK
name: String
model: String
barcode: String
quantity: Integer
initial_entry: DateTime
last_updated: DateTime
"""


class CapyTUI(App):
    TITLE = "CapyTUI"
    # CSS_PATH = "styles/main.tcss"
    BINDINGS = []
    SCREENS = {"home": Home}
    INITIAL_SCREEN = "home"

    def __init__(self):
        super().__init__()

    def on_mount(self) -> None:
        self.theme = "gruvbox"

    def on_ready(self) -> None:
        self.push_screen("home")


if __name__ == "__main__":
    CapyTUI().run()

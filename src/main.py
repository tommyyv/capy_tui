# standard
import pathlib

# framework
from textual.app import App

# user-defined
from screens.home import Home
from services.db import Database

DATABASE_PATH = pathlib.Path().home() / "dev/infra/db/capy_tui/in_memory.db"


class CapyTUI(App):
    CSS = """
    .with-border {
        border: heavy green;
    }
    """

    # CSS_PATH = "styles/main.tcss"
    TITLE = "CapyTUI"

    def __init__(self, db_path):
        super().__init__()
        self.db: Database = Database(db_path)

    def on_mount(self) -> None:
        self.theme = "gruvbox"
        self.push_screen(Home(self.db))


if __name__ == "__main__":
    app = CapyTUI(DATABASE_PATH)
    app.run()

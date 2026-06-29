# standard

# framework
from textual.app import App

# user-defined
from infrastructure.database import Database
from infrastructure.sqlite_repository import SQLiteRepository
from ui.home import HomeScreen


class CapyTUI(App):
    """Main application class."""

    TITLE = "CAPY TUI"
    CSS_PATH = "styles/main.tcss"

    def __init__(self):
        super().__init__()
        # Initialize database and repository
        self.db = Database("assets.db")
        self.repository = SQLiteRepository(self.db)

        # Initialize schema
        self.db.initialize_schema()

    def on_mount(self) -> None:
        """Called when app is mounted."""
        self.push_screen(HomeScreen(self.repository))


if __name__ == "__main__":
    app = CapyTUI()
    app.run()

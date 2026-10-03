# standard
from pathlib import Path

# framework
from textual.app import App

# user-defined
from capy_tui.application.asset_workflow import AssetWorkflow
from capy_tui.application.csv_service import CSVService
from capy_tui.infrastructure.database import Database
from capy_tui.infrastructure.sqlite_repository import SQLiteRepository
from capy_tui.ui.home import HomeScreen


class CapyTUI(App):
    TITLE = "CAPY TUI"
    CSS_PATH = "styles/main.tcss"

    def __init__(self, db_path: Path):
        super().__init__()

        # infrastructure
        self.db = Database(db_path=db_path)
        self.repository = SQLiteRepository(self.db)
        self.db.initialize_schema()

        # Application services & workflows
        self.asset_workflow = AssetWorkflow(self.repository)
        self.csv_service = CSVService()

        # UI
        self.home_screen = HomeScreen(
            asset_workflow=self.asset_workflow,
            repository=self.repository,
            csv_service=self.csv_service,
        )

    def on_mount(self) -> None:
        self.push_screen(self.home_screen)

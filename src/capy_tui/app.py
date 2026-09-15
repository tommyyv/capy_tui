# standard
from pathlib import Path

# framework
from textual.app import App

# user-defined
from capy_tui.application.asset_workflow import AssetWorkflow
from capy_tui.application.csv_service import CSVService
from capy_tui.infrastructure.database import Database
from capy_tui.infrastructure.sqlite_repository import SQLiteRepository
from capy_tui.ui.excess_screen import ExcessScreen
from capy_tui.ui.home import HomeScreen
from capy_tui.ui.import_screen import ImportScreen
from capy_tui.ui.scan_screen import ScanScreen


class CapyTUI(App):
    """Main application class."""

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
        self.home_screen = HomeScreen()
        self.scan_screen = ScanScreen(asset_workflow=self.asset_workflow)
        self.excess_screen = ExcessScreen(repository=self.repository)
        self.import_screen = ImportScreen(
            asset_workflow=self.asset_workflow, csv_service=self.csv_service
        )

    def on_mount(self) -> None:
        """Called when app is mounted."""
        self.push_screen(self.home_screen)

    def show_scan(self) -> None:
        self.switch_screen(self.scan_screen)

    def show_inventory(self) -> None:
        pass

    def show_excess(self) -> None:
        pass

    def show_import(self) -> None:
        self.switch_screen(self.import_screen)

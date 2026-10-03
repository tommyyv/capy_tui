# standard

# framework
from textual.app import ComposeResult
from textual.containers import Vertical, Center
from textual.screen import Screen
from textual.widgets import Header, Button, Static, Footer

# user-defined
from capy_tui.application.asset_workflow import AssetWorkflow
from capy_tui.application.csv_service import CSVService
from capy_tui.infrastructure.sqlite_repository import SQLiteRepository
from capy_tui.ui.import_screen import ImportScreen
from capy_tui.ui.scan_screen import ScanScreen
from capy_tui.ui.excess_screen import ExcessScreen


class HomeScreen(Screen):
    """Main menu screen."""

    BINDINGS = [
        ("s", "open_scan", "Scan"),
        ("i", "open_import", "Import"),
        ("e", "open_excess", "Excess"),
        ("escape", "quit", "Quit"),
    ]

    def __init__(
        self,
        asset_workflow: AssetWorkflow,
        repository: SQLiteRepository,
        csv_service: CSVService,
    ):
        super().__init__()

        self.asset_workflow = asset_workflow
        self.repository = repository
        self.csv_service = csv_service

    def compose(self) -> ComposeResult:
        yield Header()

        with Vertical():
            yield Static("Capy TUI", classes="title")
            yield Static("Choose an option:", classes="subtitle")

            with Center():
                yield Button(
                    "Scan Assets",
                    id="scan-btn",
                    variant="primary",
                )

                yield Button(
                    "View Inventory",
                    id="inventory-btn",
                    variant="success",
                )

                yield Button(
                    "Excess Assets",
                    id="excess-btn",
                    variant="warning",
                )

                yield Button(
                    "Import CSV",
                    id="import-btn",
                    variant="primary",
                )

        yield Footer()

    def action_open_scan(self) -> None:
        self.app.push_screen(
            ScanScreen(
                asset_workflow=self.asset_workflow,
            )
        )

    def action_open_excess(self) -> None:
        self.app.push_screen(
            ExcessScreen(
                asset_workflow=self.asset_workflow,
                csv_service=self.csv_service,
            )
        )

    def action_open_import(self) -> None:
        self.app.push_screen(
            ImportScreen(
                asset_workflow=self.asset_workflow,
                csv_service=self.csv_service,
            )
        )

    # TODO: use a strategy pattern to select between the screen depending on the event.id
    """
    this is what it should be like:

    type CallableFn = Callable[str, None]

    screener: dict[str, CallableFn] = {}
    screen_select = {
        "scan-btn": self.action_open_import
    }

    then the method would be: if the event id is X, then use the dictionary to choose the associated method

    should i use a switch or a control branch to check the event.id
    if event.button.id:
        screen[event.button.id]

    """

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "scan-btn":
            self.action_open_scan()

        elif event.button.id == "inventory-btn":
            # NOTE: i dont think i need this
            pass

        elif event.button.id == "excess-btn":
            self.action_open_excess()

        elif event.button.id == "import-btn":
            self.action_open_import()

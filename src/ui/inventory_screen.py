# standard

# framework
from textual.app import ComposeResult
from textual.screen import ModalScreen
from textual.widgets import Header, Footer, DataTable, Button, Input, Label
from textual.containers import Container, Horizontal, Vertical
from textual import on

# user-defined
from domain import asset_ops


class InventoryScreen(ModalScreen):
    """Screen for viewing inventory."""

    BINDINGS = [
        ("escape", "app.pop_screen", "Back"),
        ("ctrl+r", "refresh_table", "Refresh"),
        ("ctrl+e", "export_csv", "Export"),
    ]

    def __init__(self, repository):
        super().__init__()
        self.repository = repository

    def compose(self) -> ComposeResult:
        """Create child widgets for the inventory screen."""
        yield Header()

        with Container():
            with Vertical():
                yield DataTable(id="inventory-table")
            with Vertical():
                yield Label("DOE Barcode:")
                yield Input(placeholder="Scan DOE barcode...", id="barcode-input")

                yield Label("MAC Address:")
                yield Input(placeholder="Scan MAC address...", id="mac-input")

            with Horizontal():
                yield Button("Search", id="search-btn", variant="success")
                yield Button("Back", id="back-btn", variant="default")

        # yield Button("EXPORT", id="export")
        # yield Button("REFRESH", id="refresh")
        yield Footer()

    def on_mount(self) -> None:
        """Called when the widget is mounted."""
        self.setup_data_table()
        self.refresh_table()

    def setup_data_table(self) -> None:
        """Setup the data table."""
        table = self.query_one(DataTable)
        table.add_columns(
            "DOE Barcode",
            "MAC Address",
            "Status",
            "Created",
            "Updated",
        )
        table.cursor_type = "row"

    def refresh_table(self) -> None:
        """Refresh the data table with current assets."""
        table = self.query_one(DataTable)
        table.clear()

        assets = asset_ops.find_all_assets(self.repository)
        for asset in assets:
            table.add_row(
                asset.barcode,
                asset.mac_address,
                asset.status.value,
                asset.created_timestamp.strftime("%Y-%m-%d %H:%M"),
                asset.updated_timestamp.strftime("%Y-%m-%d %H:%M"),
            )

    def action_refresh_table(self) -> None:
        """Action to refresh the table."""
        self.refresh_table()

    def search_assets(self) -> None:
        # TODO: (bug) fix search by doe or mac
        """Search for assets."""
        search_input = (
            self.query_one("#barcode-input", Input).value
            or self.query_one("#mac-input", Input).value
        )

        if not search_input:
            self.notify("Please enter a search term", severity="warning")
            return

        assets = asset_ops.find_asset_by_search_term(self.repository, search_input)
        if not assets:
            self.notify("No assets found", severity="info")
            return

        table = self.query_one(DataTable)
        table.clear()
        for asset in assets:
            table.add_row(
                asset.barcode,
                asset.mac_address,
                asset.status.value,
                asset.created_timestamp.strftime("%Y-%m-%d %H:%M"),
                asset.updated_timestamp.strftime("%Y-%m-%d %H:%M"),
            )

    @on(Input.Submitted, "#mac-input")
    @on(Input.Submitted, "#barcode-input")
    @on(Button.Pressed, "#search-btn")
    def on_input_submitted(self) -> None:
        """Handle input submissions.
        Press enter after the mac input or click the ADD ASSET button."""
        # self.current_barcode: str = self.query_one("#barcode-input", Input).value
        # self.current_mac: str = self.query_one("#mac-input", Input).value

        # if self.current_barcode or self.current_mac:
        self.query(Input).focus()
        self.search_assets()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses."""
        if event.button.id == "back-btn":
            self.app.pop_screen()

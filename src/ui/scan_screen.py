# standard
import csv
from datetime import datetime

# framework
from textual.app import ComposeResult
from textual.screen import ModalScreen
from textual.widgets import Header, Footer, DataTable, Input, Button, Label
from textual.containers import Container, Vertical, Horizontal
from textual import on

# user-defined
from domain.asset import AssetStatus
from domain import asset_ops


class ScanScreen(ModalScreen):
    """Screen for scanning assets."""

    BINDINGS = [
        ("escape", "app.pop_screen", "Back"),
        ("ctrl+r", "refresh_table", "Refresh"),
        ("ctrl+e", "export_csv", "Export"),
    ]

    def __init__(self, repository):
        super().__init__()
        self.repository = repository
        self.current_barcode = ""
        self.current_mac = ""

    def compose(self) -> ComposeResult:
        """Create child widgets for the scan screen."""
        yield Header()

        with Container():
            with Vertical():
                yield Label("Scan Assets", classes="title")

                with Vertical():
                    yield Label("DOE Barcode:")
                    yield Input(placeholder="Scan DOE barcode...", id="barcode-input")

                    yield Label("MAC Address:")
                    yield Input(placeholder="Scan MAC address...", id="mac-input")

                with Horizontal():
                    yield Button("Add Asset", id="add-btn", variant="primary")
                    yield Button("Update", id="update-btn", variant="warning")
                    yield Button("Delete", id="delete-btn", variant="error")
                    yield Button("Back", id="back-btn", variant="default")

                yield DataTable(id="assets-table")

        yield Footer()

    def on_mount(self) -> None:
        """Called when the widget is mounted."""
        self.query_one("#barcode-input").focus()
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

    @on(Input.Submitted, "#mac-input")
    @on(Button.Pressed, "#add-btn")
    def on_input_submitted(self) -> None:
        """Handle input submissions.
        Press enter after the mac input or click the ADD ASSET button."""
        self.current_barcode: str = self.query_one("#barcode-input", Input).value[5:]
        self.current_mac: str = self.query_one("#mac-input", Input).value.capitalize()

        if self.current_barcode and self.current_mac:
            self.query_one("#mac-input", Input).focus()
            self.add_asset()

    # NOTE: intentially using event approach because these are all the features we need
    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses."""
        if event.button.id == "add-btn":
            self.add_asset()
        # elif event.button.id == "search-btn":
        # self.search_assets()
        elif event.button.id == "update-btn":
            self.update_asset()
        elif event.button.id == "delete-btn":
            self.delete_asset()
        elif event.button.id == "back-btn":
            self.app.pop_screen()

    def add_asset(self) -> None:
        """Add an asset to the database."""
        if not self.current_barcode or not self.current_mac:
            self.notify(
                f"Please enter both DOE barcode and MAC address: entered {self.current_barcode}, {self.current_mac}",
                severity="warning",
            )
            return

        # Check if asset already exists
        existing_asset = asset_ops.find_asset_by_barcode_and_mac(
            self.repository, self.current_barcode, self.current_mac
        )

        if existing_asset:
            self.notify(
                f"Asset already exists: {existing_asset.barcode}, {existing_asset.mac_address}",
                title="Asset Exists",
                severity="warning",
            )
        else:
            # Create new asset
            asset = asset_ops.create_asset(
                self.repository, self.current_barcode, self.current_mac
            )
            self.notify(f"Asset added: {asset.barcode}")
            self.refresh_table()

        # Clear inputs for next scan
        self.query_one("#barcode-input", Input).value = ""
        self.query_one("#mac-input", Input).value = ""
        self.current_barcode = ""
        self.current_mac = ""
        self.query_one("#barcode-input").focus()

    def update_asset(self) -> None:
        """Update an asset."""
        if not self.current_barcode or not self.current_mac:
            self.notify(
                "Please enter both DOE barcode and MAC address", severity="warning"
            )
            return

        # For now, just update the status to Active
        updated_asset = asset_ops.update_asset_status(
            self.repository, self.current_barcode, self.current_mac, AssetStatus.ACTIVE
        )

        if updated_asset:
            self.notify(f"Asset updated: {updated_asset.barcode}")
            self.refresh_table()
        else:
            self.notify("Asset not found", severity="error")

    def delete_asset(self) -> None:
        """Delete an asset."""
        if not self.current_barcode or not self.current_mac:
            self.notify(
                "Please enter both DOE barcode and MAC address", severity="warning"
            )
            return

        success = asset_ops.delete_asset(
            self.repository, self.current_barcode, self.current_mac
        )

        if success:
            self.notify(f"Asset deleted: {self.current_barcode}")
            self.refresh_table()
        else:
            self.notify("Asset not found", severity="error")

    def action_refresh_table(self) -> None:
        """Action to refresh the table."""
        self.refresh_table()

    def action_export_csv(self) -> None:
        """Export current table to CSV."""
        assets = asset_ops.find_all_assets(self.repository)

        filename = f"assets_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        with open(filename, "w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(
                [
                    "DOE Barcode",
                    "MAC Address",
                    "Status",
                    "Created",
                    "Updated",
                ]
            )

            for asset in assets:
                writer.writerow(
                    [
                        asset.barcode,
                        asset.mac_address,
                        asset.status.value,
                        asset.created_timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                        asset.updated_timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                    ]
                )

        self.notify(f"Assets exported to {filename}", severity="info")

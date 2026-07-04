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
from domain.asset import Asset, AssetStatus
from domain import asset_ops


class ExcessScreen(ModalScreen):
    """Screen for managing excess assets."""

    BINDINGS = [
        ("escape", "app.pop_screen", "Back"),
        ("ctrl+r", "refresh_table", "Refresh"),
        ("ctrl+e", "export_csv", "Export"),
        ("ctrl+d", "delete_row_selected", "Delete"),
    ]

    def __init__(self, repository):
        super().__init__()
        self.repository = repository
        self.current_barcode = ""
        self.current_mac = ""

    def compose(self) -> ComposeResult:
        """Create child widgets for the excess screen."""
        yield Header()

        with Container():
            with Vertical():
                yield Label("Excess Assets", classes="title")

                with Vertical():
                    yield Label("DOE Barcode:")
                    yield Input(placeholder="Scan DOE barcode...", id="barcode-input")

                    yield Label("MAC Address:")
                    yield Input(placeholder="Scan MAC address...", id="mac-input")

                with Horizontal():
                    yield Button("Move To Excess", id="excess-btn", variant="primary")
                    yield Button("Add To Excess", id="add-btn", variant="warning")
                    yield Button("Search", id="search-btn", variant="success")

                yield DataTable(id="excess-table")

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
        """Refresh the data table with current excess assets."""
        table = self.query_one(DataTable)
        table.clear()

        assets = asset_ops.find_all_excess_assets(self.repository)
        for asset in assets:
            table.add_row(
                asset.barcode,
                asset.mac_address,
                asset.status.value,
                asset.created_timestamp.strftime("%Y-%m-%d %H:%M"),
                asset.updated_timestamp.strftime("%Y-%m-%d %H:%M"),
            )

    @on(Input.Submitted, "#mac-input")
    @on(Button.Pressed, "#excess-btn")
    @on(Button.Pressed, "#add-btn")
    def on_input_submitted(self, event: Button.Pressed) -> None:
        """Handle input submissions.
        Press enter after the mac input or click the ADD TO EXCESS button."""
        self.current_barcode: str = self.query_one("#barcode-input", Input).value[5:]
        self.current_mac: str = self.query_one("#mac-input", Input).value.upper()

        if self.current_barcode and self.current_mac:
            self.query_one("#mac-input", Input).focus()
            if event.button.id == "excess-btn":
                self.mark_excess()
            elif event.button.id == "add-btn":
                self.add_asset()

    # NOTE: do i even need this?
    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses."""
        if event.button.id == "excess-btn":
            self.mark_excess()
        elif event.button.id == "search-btn":
            self.search_assets()
        elif event.button.id == "add-btn":
            self.add_asset()
        elif event.button.id == "delete-btn":
            self.delete_asset()
        elif event.button.id == "back-btn":
            self.app.pop_screen()

    def mark_excess(self) -> None:
        """Mark an asset as excess."""
        if not self.current_barcode or not self.current_mac:
            self.notify(
                "Please enter both DOE barcode and MAC address", severity="warning"
            )
            return

        # Find the asset in the main assets table
        asset = asset_ops.find_asset_by_barcode_and_mac(
            self.repository, self.current_barcode, self.current_mac
        )

        if not asset:
            self.notify("Asset not found in inventory", severity="error")
            return

        # Update status in main table
        updated_asset = asset.update_status(AssetStatus.PENDING_EXCESS)
        self.repository.update(updated_asset)

        # Add to excess table
        excess_asset = self.repository.save_to_excess(updated_asset)

        self.notify(f"Asset marked as excess: {excess_asset.barcode}")
        self.refresh_table()

        # Clear inputs
        self.query_one("#barcode-input", Input).value = ""
        self.query_one("#mac-input", Input).value = ""
        self.current_barcode = ""
        self.current_mac = ""
        self.query_one("#barcode-input").focus()

    def search_assets(self) -> None:
        """Search for excess assets."""
        search_input = self.query_one("#barcode-input", Input).value
        if not search_input:
            self.notify("Please enter a search term", severity="warning")
            return

        # Search in excess table
        results = self.repository.search(search_input)

        table = self.query_one(DataTable)
        table.clear()
        for asset in results:
            table.add_row(
                asset.barcode,
                asset.mac_address,
                asset.status.value,
                asset.created_timestamp.strftime("%Y-%m-%d %H:%M"),
                asset.updated_timestamp.strftime("%Y-%m-%d %H:%M"),
            )

    def add_asset(self) -> None:
        """Add an asset to the excess table."""
        if not self.current_barcode or not self.current_mac:
            self.notify(
                "Please enter both DOE barcode and MAC address", severity="warning"
            )
            return

        # Create a new asset and mark as excess

        asset = Asset.create_new(self.current_barcode, self.current_mac)
        excess_asset = asset.update_status(AssetStatus.PENDING_EXCESS)

        # Save to excess table
        saved_asset = self.repository.save_to_excess(excess_asset)

        self.notify(f"Asset added to excess: {saved_asset.barcode}")
        self.refresh_table()

        # Clear inputs
        self.query_one("#barcode-input", Input).value = ""
        self.query_one("#mac-input", Input).value = ""
        self.current_barcode = ""
        self.current_mac = ""
        self.query_one("#barcode-input").focus()

    def delete_asset(self) -> None:
        """Delete an asset from the excess table."""
        if not self.current_barcode or not self.current_mac:
            self.notify(
                "Please enter both DOE barcode and MAC address", severity="warning"
            )
            return

        success = self.repository.delete_from_excess_by_barcode_and_mac(
            self.current_barcode, self.current_mac
        )

        if success:
            self.notify(f"Asset removed from excess: {self.current_barcode}")
            self.refresh_table()
        else:
            self.notify("Asset not found in excess table", severity="error")

    def action_delete_asset(self) -> None:
        self.delete_asset()

    def action_refresh_table(self) -> None:
        """Action to refresh the table."""
        self.refresh_table()

    def action_export_csv(self) -> None:
        """Export current excess table to CSV."""
        # Get excess assets from database
        with self.repository.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM excess_assets ORDER BY updated_timestamp DESC"
            )
            results = cursor.fetchall()

        filename = f"excess_assets_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
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

            for row in results:
                writer.writerow(
                    [
                        row["barcode"],
                        row["mac_address"],
                        row["status"],
                        row["created_timestamp"],
                        row["updated_timestamp"],
                    ]
                )

        self.notify(f"Excess assets exported to {filename}", severity="info")

    def action_delete_row_selected(self) -> None:
        table = self.query_one(DataTable)

        # Check if a row is actually selected/cursor is active
        if table.cursor_coordinate is not None:
            # Convert coordinate to row_key
            row_key, _ = table.coordinate_to_cell_key(table.cursor_coordinate)
            if row_key:
                doe = table.get_row(row_key)[0]
                mac = table.get_row(row_key)[1]

                self.repository.delete_from_excess_by_barcode_and_mac(doe, mac)

                table.remove_row(row_key)

                self.refresh_table()

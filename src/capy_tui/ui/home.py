# standard

# framework
from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Header, Button, Static
from textual.containers import Vertical, Center

# user-defined


class HomeScreen(Screen):
    """Home screen with navigation options."""

    def compose(self) -> ComposeResult:
        """Create child widgets for the home screen."""
        yield Header()

        with Vertical():
            yield Static("Capy TUI", classes="title")
            yield Static("Choose an option:", classes="subtitle")

            with Center():
                yield Button("Scan Assets", id="scan-btn", variant="primary")
                yield Button("View Inventory", id="inventory-btn", variant="success")
                yield Button("Excess Assets", id="excess-btn", variant="warning")
                yield Button("Import CSV", id="import-btn", variant="primary")

        # TODO: add bindings to footer
        # yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses."""
        if event.button.id == "scan-btn":
            self.app.show_scan()
        elif event.button.id == "inventory-btn":
            self.app.show_scan()
        elif event.button.id == "excess-btn":
            self.app.push_screen(self.excess_screen)
        elif event.button.id == "import-btn":
            self.app.show_import()

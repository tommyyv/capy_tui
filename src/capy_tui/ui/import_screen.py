from pathlib import Path

from textual.app import ComposeResult
from textual.containers import Container, Vertical
from textual.screen import Screen
from textual import on
from textual.widgets import (
    Button,
    DataTable,
    Footer,
    Header,
    Input,
    Label,
)

from application.asset_workflow import AssetWorkflow
from application.csv_service import CSVService


class ImportScreen(Screen):
    """UI for importing assets from CSV.

    CSV file via import button (UI)
       v
    CSVService.read_csv()
       v
    normalized dictionaries
       v
    AssetWorkflow.import_assets()
       v
    AssetWorkflow.create_new()
       v
    Repository.save()
       v
    SQLite (Database)
    """

    BINDINGS = [
        ("escape", "app.pop_screen", "Back"),
    ]

    def __init__(
        self,
        csv_service: CSVService,
        asset_workflow: AssetWorkflow,
    ) -> None:
        super().__init__()

        self.csv_service = csv_service
        self.asset_workflow = asset_workflow

        self.selected_file: Path | None = None

    def compose(self) -> ComposeResult:
        yield Header()

        with Container():
            yield Label("Import Assets", classes="title")

            with Vertical():
                yield Input(
                    placeholder="Path to CSV file...",
                    id="csv-path",
                )

                yield Button(
                    "Preview",
                    id="preview-btn",
                    variant="default",
                )

                yield Button(
                    "Import",
                    id="import-btn",
                    variant="success",
                )

            yield DataTable(id="preview-table")

        yield Footer()

    def on_mount(self) -> None:
        table = self.query_one("#preview-table", DataTable)

        table.cursor_type = "row"

    @on(Button.Pressed, "#preview-btn")
    def preview_csv(self) -> None:
        """Read and display CSV data without importing it."""

        path_input = self.query_one("#csv-path", Input)

        if not path_input.value.strip():
            self.notify(
                "Please select a CSV file.",
                severity="warning",
            )
            return

        path = Path(path_input.value.strip())

        try:
            rows = self.csv_service.read_csv(path)

            self.preview_rows = rows
            self.selected_file = path

            self._render_preview(rows)

            self.notify(
                f"Previewing {len(rows)} rows.",
                severity="information",
            )

        except (FileNotFoundError, ValueError) as exc:
            self.notify(
                str(exc),
                severity="error",
            )

            # except UnicodeDecodeError:
            self.notify(
                "CSV must be UTF-8 encoded.",
                severity="error",
            )

    @on(Button.Pressed, "#import-btn")
    def import_csv(self) -> None:
        """Import CSV data through the asset workflow."""

        if self.selected_file is None:
            self.notify(
                "Preview a CSV file before importing.",
                severity="warning",
            )
            return

        try:
            rows = self.csv_service.read_csv(self.selected_file)

            assets = self.asset_workflow.import_assets(rows)

            self.notify(
                f"Successfully imported {len(assets)} assets.",
                severity="information",
            )

            self.preview_rows.clear()

            table = self.query_one(
                "#preview-table",
                DataTable,
            )
            table.clear()

        except (FileNotFoundError, ValueError) as exc:
            self.notify(
                str(exc),
                severity="error",
            )

            # except UnicodeDecodeError:
            self.notify(
                "CSV must be UTF-8 encoded.",
                severity="error",
            )

    def _render_preview(
        self,
        rows: list[dict[str, str | None]],
    ) -> None:
        """Render normalized CSV data in the UI."""

        table = self.query_one(
            "#preview-table",
            DataTable,
        )

        table.clear()

        if not rows:
            return

        # TODO: make dynamic
        headers = [
            "building",
            "room",
            "asset_tag",
            "mac_address",
        ]

        table.add_columns(*headers)

        for row in rows[:50]:
            table.add_row(
                row["building"] or "",
                row["room"] or "",
                row["asset_tag"] or "",
                row["mac_address"] or "",
            )

from pathlib import Path

from textual.app import ComposeResult
from textual.containers import Container, Vertical, Horizontal
from textual.screen import ModalScreen, Screen
from textual import on
from textual.widgets import (
    Button,
    Footer,
    Header,
    Input,
    Label,
    DirectoryTree,
)

from capy_tui.application.asset_workflow import AssetWorkflow
from capy_tui.application.csv_service import CSVService


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

                # yield Button(
                #     "Preview",
                #     id="preview-btn",
                #     variant="default",
                # )

                yield Button(
                    "Import",
                    id="import-btn",
                    variant="success",
                )

            # yield DataTable(id="preview-table")

        # yield DirectoryTree("./data")
        yield DirectoryTree("./mock/")
        yield Footer()

    def on_mount(self) -> None:
        pass
        # table = self.query_one("#preview-table", DataTable)

        # table.cursor_type = "row"

    @on(DirectoryTree.FileSelected)
    def on_file_selected(self, event: DirectoryTree.FileSelected) -> None:
        path = event.path

        # self.selected_file = path
        self.query_one("#csv-path", Input).value = str(path)

        # if not self.selected_file.value.strip():
        #     self.notify(
        #         "Please select a CSV file.",
        #         severity="warning",
        #     )
        # return

    # @on(Button.Pressed, "#preview-btn")
    # def preview_csv(self) -> None:
    #     """Read and display CSV data without importing it."""
    #
    #     path_input = self.query_one("#csv-path", Input).value
    #     try:
    #         rows = self.csv_service.read_csv(Path(path_input))
    #
    #         self.preview_rows = rows
    #         # self.selected_file = path_input
    #
    #         self._render_preview(rows)
    #
    #         self.notify(
    #             f"Previewing {len(rows)} rows.",
    #             severity="information",
    #         )
    #
    #     except (FileNotFoundError, ValueError) as exc:
    #         self.notify(
    #             str(exc),
    #             severity="error",
    #         )
    #
    #         # except UnicodeDecodeError:
    #         self.notify(
    #             "CSV must be UTF-8 encoded.",
    #             severity="error",
    #         )

    @on(Button.Pressed, "#import-btn")
    def import_csv(self) -> None:
        """Import CSV data through the asset workflow."""

        file = Path(self.query_one("#csv-path", Input).value)
        self.notify(f"selected file: {file}")

        if file is None:
            self.notify(
                "Preview a CSV file before importing.",
                severity="warning",
            )
            return

        try:
            rows = self.csv_service.read_csv(file)

            assets = self.asset_workflow.import_assets(rows)

            self.notify(
                f"Successfully imported {len(assets)} assets.",
                severity="information",
            )

            # self.preview_rows.clear()

            # table = self.query_one(
            #     "#preview-table",
            #     DataTable,
            # )
            # table.clear()

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

    # def _render_preview(
    #     self,
    #     rows: list[dict[str, str | None]],
    # ) -> None:
    #     """Render normalized CSV data in the UI."""
    #
    #     table = self.query_one(
    #         "#preview-table",
    #         DataTable,
    #     )
    #
    #     table.clear()
    #
    #     if not rows:
    #         return
    #
    #     # TODO: make dynamic
    #     headers = [
    #         "building",
    #         "room",
    #         "asset_tag",
    #         "mac_address",
    #     ]
    #
    #     table.add_columns(*headers)
    #
    #     for row in rows[:50]:
    #         table.add_row(
    #             row["building"] or "",
    #             row["room"] or "",
    #             row["asset_tag"] or "",
    #             row["mac_address"] or "",
    #         )


# NOTE: i think this class object needs to be on the home screen because there'll be an action_import that will push
# this modal screen when the import button is pressed. home > import_btn > import modal

"""
FEATURES:
    - import
    - preview
    - directory tree
    - cancel

REQUIREMENTS:
    - select file from directory tree, highlighting selection
    - import select file
    - cancel -> closes the modal screen
    - preview the data before importing

CONSTRAINTS:
    - root path is: ./data/
    - file must be csv
    - file must a be file

UTILITY:
    - validate file extension
    - validate file existence
    - must be selecting a file within the directory

user presses the import button from the home screen. a modal pops open; the user comes across a directory tree with 3
buttons (import, preview, cancel)
"""


class ImportModalScreen(ModalScreen):
    """UI for importing assets from CSV.

    CSV file via import button (UI)
       v
    CSVService.read_csv(selected_file_path) -> normalized data
       v
    [AssetWorkflow.create_new(asset for asset in assets)]
       v
    Repository.save(assets)
       v
    SQLite (Database)
    """

    def __init__(self, csv_service: CSVService, asset_workflow: AssetWorkflow) -> None:
        self.csv_service = csv_service
        self.asset_workflow = asset_workflow

    def compose(self) -> ComposeResult:
        yield Header()

        with Container():
            yield Label("Import Assets", classes="title")

            with Vertical():
                yield Input(
                    placeholder="Path to CSV file...",
                    id="csv-path",
                )

            with Horizontal(id="button-row"):
                yield Button("Preview", id="preview-btn", variant="primary")
                yield Button("Import", id="import-btn", variant="success")
                yield Button("Cancel", id="cancel-btn", variant="error")

        # NOTE: change when testing
        yield DirectoryTree("./mock/")
        yield Footer()

    def on_mount(self) -> None:
        self.query_one("#dir-tree", DirectoryTree).focus()

    def on_directory_tree_file_selected(
        self, event: DirectoryTree.FileSelected
    ) -> None:
        # TODO: assign the event.id to the file_path variable that is currently none
        pass

    # TODO: use service workflows to validate
    @on(Button.Pressed)
    def on_preview(self):
        # TODO: opens a datatable -> how though?
        pass

    @on(Button.Pressed, "#cancel-btn")
    def on_cancel(self):
        # TODO: because I'm pushing a screen from the home screen, i can pop it off when I'm done.
        self.app.pop_screen()

    @on(Button.Pressed)
    def on_import(self):
        # TODO: use csv_service to import or an importer_service that takes a specific file type -> for
        # now use csv_service to import the csv file -> scale later

        # TODO: add file_path: Path from the highlighted selecton in the directory tree
        # NOTE: this comes from the on_directory_tree_file_selected. take the value and assign it to a local
        # variable
        # TODO: pass file_path as an arguent into the service -> what type of data are the rows?
        rows = self.csv_service.read_csv()

        # TODO: what am i doing with this data? -> take data and store it into the database -> can i create
        # multiple sqlite databases and mount them by choice?

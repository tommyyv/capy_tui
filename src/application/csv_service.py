# standard
import csv
from pathlib import Path
# framework

# user-defined
from domain.asset import Asset
from infrastructure.sqlite_repository import SQLiteRepository
from .asset_workflow import AssetWorkflow

# ✓ Read CSV
# ✓ Validate CSV structure
# ✓ Normalize CSV data
# ✓ Convert rows → Assets/data
# ✓ Export Assets → CSV
# ✓ Import through workflow


class CSVService:
    """
    Static:
        - validate
        - normalize

    Public:
        - import
        - export
    """

    def __init__(self, repo: SQLiteRepository, asset_workflow: AssetWorkflow) -> None:
        self.repo = repo
        self.workflow = asset_workflow

    def import_csv(self, file_path: Path) -> list[Asset]:
        # NOTE (STEP): get csv path
        # NOTE (STEP): validate csv
        # NOTE (STEP): normalized csv
        # NOTE (STEP): create normalized object
        # NOTE (STEP): save to the repo

        # open csv file_path
        with open(file_path, "r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                # extract each rows
                building = row.get("building", "").strip()
                room = row.get("room", "").strip()
                asset_tag = row.get("asset_tag", "").strip()
                mac_address = row.get("mac_address", "").strip()

                # TODO: create an asset for each row in the csv file
                # NOTE: no need to return anything..maybe if i return something, then it's for
                # logs
                # NOTE: can my create_asset do this: unpack the csv rows, instantiate an
                # Asset object and pass the csv rows (data) into the object's constructor. do
                # this for each row in the reader object.
                # NOTE: where should my input validation be? i think it's already done elsewhere
                self.workflow.create_asset(
                    self.repo, building, room, asset_tag, mac_address
                )

            return True

    def export_csv(self, file_path: Path, assets: list[Asset]) -> None:
        # NOTE (STEP): get assets
        # NOTE (STEP): prep csv rows
        # NOTE (STEP): write to csv file
        pass

    # NOTE: I don't think I need this?
    @staticmethod
    def _validate_csv(file_path: str) -> bool:
        # must be a valid path
        path = Path(file_path)

        if not path.exists():
            pass

        # must be a file
        if not path.is_file():
            pass

        # must be csv file format
        if path.suffix.lower() != ".csv":
            pass

        return True

    @staticmethod
    def _normalize_row(row: dict[str, str]) -> dict[str, str]:
        return {
            "building": row.get("building", "").strip(),
            "room": row.get("room", "").strip(),
            "asset_tag": row.get("asset_tag", "").strip(),
            "mac_address": row.get("mac_address", "").strip(),
        }

    # def preview_csv_data(self) -> None:
    #     """Preview the CSV data in the table."""
    #     try:
    #         # Clear and reset the preview table
    #         preview_table = self.query_one("#preview-table", DataTable)
    #         preview_table.visible = True
    #         preview_table.clear()
    #
    #         # Read the CSV file
    #         with open(
    #             self.selected_file_path, "r", newline="", encoding="utf-8"
    #         ) as csvfile:
    #             reader = csv.DictReader(csvfile)
    #
    #             # Add columns based on CSV headers
    #             if reader.fieldnames:
    #                 preview_table.add_columns(*reader.fieldnames)
    #
    #             # Add rows (limit to first 50 for performance)
    #             row_count = 0
    #             for row in reader:
    #                 if row_count >= 50:  # Limit preview to first 50 rows
    #                     break
    #                 preview_table.add_row(
    #                     *[row.get(field, "") for field in reader.fieldnames]
    #                 )
    #                 row_count += 1
    #
    #             # Store the data for potential import
    #             self.imported_data = list(
    #                 csv.DictReader(open(self.selected_file_path, "r", encoding="utf-8"))
    #             )
    #
    #         self.notify(
    #             f"Previewing {min(len(self.imported_data), 50)} rows from {self.selected_file_path}",
    #             severity="info",
    #         )
    #
    #     except UnicodeDecodeError:
    #         self.notify(
    #             "Invalid file encoding. Please ensure the file is UTF-8 encoded.",
    #             severity="error",
    #         )
    #         self.query_one("#preview-table", DataTable).visible = False
    #     except Exception as e:
    #         self.logger.error(f"Error previewing CSV data: {e}")
    #         self.notify(f"Error previewing CSV: {e}", severity="error")
    #         self.query_one("#preview-table", DataTable).visible = False

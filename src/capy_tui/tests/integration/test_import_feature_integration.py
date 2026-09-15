# standard
from pathlib import Path
import unittest

# framework

# user-defined
from capy_tui.application.asset_workflow import AssetWorkflow
from capy_tui.application.csv_service import CSVService
from capy_tui.infrastructure.sqlite_repository import SQLiteRepository
from capy_tui.infrastructure.database import Database


class TestAssetImportIntegration(unittest.TestCase):
    def setUp(self) -> None:
        pass

    def test_import_assets_from_csv(self):
        pass


if __name__ == "__main__":
    unittest.main()


db_path = Path("mock") / "mock_db.db"
csv_path = Path("mock") / "mock_csv_two.csv"
# print("Working directory:", Path.cwd())
# print("Attempted path:", csv_path)
# print("Absolute path:", csv_path.resolve())
# print("Exists:", csv_path.exists())
# print(csv_path)

db = Database(db_path=db_path)
repo = SQLiteRepository(db)
db.initialize_schema()
csv_service = CSVService()
asset_workflow = AssetWorkflow(repo)

rows = csv_service.read_csv(csv_path)
assets = asset_workflow.import_assets(rows)
print(assets)

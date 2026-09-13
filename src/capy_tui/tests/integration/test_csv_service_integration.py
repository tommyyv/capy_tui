# standard
from pathlib import Path

# framework

# user-defined
from domain.asset import Asset
from infrastructure.database import Database
from infrastructure.sqlite_repository import SQLiteRepository
from application.asset_workflow import AssetWorkflow
from application.csv_service import CSVService

# ✓ Read CSV
# ✓ Validate CSV structure
# ✓ Normalize CSV data
# ✓ Convert rows → Assets/data
# ✓ Export Assets → CSV
# ✓ Import through workflow

# INTEGRATION TEST
test_csv = Path("mock/mock_csv.csv")
test_export_csv_file = Path("data/mock_exported_csv.csv")

test_db = Database("mock/mock_db.db")
test_repo = SQLiteRepository(database=test_db)
test_db.initialize_schema()

test_asset_workflow = AssetWorkflow(repo=test_repo)
test_csv_service = CSVService()

# (TEST): create function => works
# test_assets: list[Asset] = [
#     test_asset_workflow.create_asset(
#         building="1234",
#         room="999",
#         asset_tag="000001234567",
#         mac_address="e01aeaaabb00",
#     ),
#     test_asset_workflow.create_asset(
#         building="5678",
#         room="111",
#         asset_tag="000009988777",
#         mac_address="e01aeaaabb11",
#     ),
# ]


# NOTE (TEST): should test normalize, validate, and import methods => this works
imported_csv = test_csv_service.read_csv(file_path=test_csv)

# NOTE (TEST): the workflow gets the normalized csv data and creates assets from them => works
assets = test_asset_workflow.import_assets(imported_csv)

# (TEST): should return all the assets that we just created above => this works
test_find_all_assets: list[Asset] = test_asset_workflow.find_all_assets()

# NOTE (TEST): should test export methods => this works
exported_csv = test_csv_service.export_csv(
    file=test_export_csv_file, assets=test_find_all_assets
)

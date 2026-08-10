# standard
from typing import List, Optional

# framework

# user-defined
from domain.asset import Asset, AssetStatus
from infrastructure.sqlite_repository import SQLiteRepository

# ✓ Create asset
# ✓ Move asset to excess
# ✓ Assign MAC
# ✓ Retire asset
# ✓ Other application-level asset operations


class AssetWorkflow:
    def __init__(self, repo: SQLiteRepository):
        self.repo = repo

    def __post_init__(self):
        pass

    def find_asset_by_barcode_and_mac(
        self, repository: SQLiteRepository, barcode: str, mac_address: str
    ) -> Optional[Asset]:
        """Find an asset by barcode and MAC address."""
        return repository.find_by_barcode_and_mac(barcode, mac_address)

    def find_all_assets(self, repository: SQLiteRepository) -> List[Asset]:
        """Get all assets from the repository."""
        return repository.get_all()

    def find_all_excess_assets(self, repository: SQLiteRepository) -> List[Asset]:
        return repository.get_all_excess()

    def create_asset(
        self,
        repository: SQLiteRepository,
        building: str,
        room: str,
        asset_tag: str,
        mac_address: str,
    ) -> Asset:
        """Create a new asset."""
        asset = Asset.create_new(building, room, asset_tag, mac_address)
        return repository.save(asset)

    def update_asset_status(
        self,
        repository: SQLiteRepository,
        barcode: str,
        mac_address: str,
        new_status: AssetStatus,
    ) -> Optional[Asset]:
        """Update an asset's status."""
        asset = self.find_asset_by_barcode_and_mac(repository, barcode, mac_address)
        if asset:
            updated_asset = asset.update_status(new_status)
            return repository.update(updated_asset)
        return None

    def delete_asset(
        self, repository: SQLiteRepository, barcode: str, mac_address: str
    ) -> bool:
        """Delete an asset."""
        return repository.delete_by_barcode_and_mac(barcode, mac_address)

    def find_asset_by_search_term(
        self, repository: SQLiteRepository, search_term: str
    ) -> List[Asset]:
        """Find assets by search term (barcode or MAC address)."""
        return repository.search(search_term)

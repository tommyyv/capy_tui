# standard
from typing import Optional
from datetime import datetime

# framework

# user-defined
from domain.asset import Asset, AssetStatus
from infrastructure.sqlite_repository import SQLiteRepository


class AssetWorkflow:
    def __init__(self, repo: SQLiteRepository):
        self.repo = repo

    def find_asset_by_barcode_and_mac(
        self,
        barcode: str,
        mac_address: str,
    ) -> Optional[Asset]:
        """Find an asset by barcode and MAC address."""
        return self.repo.find_by_barcode_and_mac(
            barcode,
            mac_address,
        )

    def find_all_assets(self) -> list[Asset]:
        """Get all assets from the repository."""
        return self.repo.get_all()

    def find_all_excess_assets(self) -> list[Asset]:
        """Get all excess assets."""
        return self.repo.get_all_excess()

    def create_asset(
        self,
        building: str | None,
        room: str | None,
        asset_tag: str,
        mac_address: str | None,
    ) -> Asset:
        now = datetime.now()

        asset = Asset(
            building=building,
            room=room,
            asset_tag=asset_tag,
            mac_address=mac_address,
            status=AssetStatus.IN_STOCK,
            created_timestamp=now,
            updated_timestamp=now,
        )

        return self.repo.save(asset)

    def update_asset_status(
        self,
        barcode: str,
        mac_address: str,
        new_status: AssetStatus,
    ) -> Optional[Asset]:
        """Update an asset's status."""
        asset = self.find_asset_by_barcode_and_mac(
            barcode,
            mac_address,
        )

        if asset is None:
            return None

        updated_asset = asset.update_status(new_status)

        return self.repo.update(updated_asset)

    def delete_asset(
        self,
        barcode: str,
        mac_address: str,
    ) -> bool:
        """Delete an asset."""
        return self.repo.delete_by_barcode_and_mac(
            barcode,
            mac_address,
        )

    def find_asset_by_search_term(
        self,
        search_term: str,
    ) -> list[Asset]:
        """Find assets by search term."""
        return self.repo.search(search_term)

    def import_assets(
        self,
        rows: list[dict[str, str | None]],
    ) -> list[Asset]:
        """Create and persist assets from normalized import data."""

        assets: list[Asset] = []

        for row in rows:
            asset = self.create_asset(
                building=row["building"],
                room=row["room"],
                asset_tag=row["asset_tag"] or "",
                mac_address=row["mac_address"],
            )

            assets.append(asset)

        return assets

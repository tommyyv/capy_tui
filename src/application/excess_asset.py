# asset_manager/workflows/excess_asset.py
from typing import Optional
from domain.asset import Asset, AssetStatus
from infrastructure.sqlite_repository import SQLiteRepository
from domain import asset_ops


def mark_asset_as_excess(
    repository: SQLiteRepository, barcode: str, mac_address: str
) -> Optional[Asset]:
    """
    Mark an asset as excess.
    Returns the updated asset if successful, None if not found.
    """
    # Find the asset in main table
    asset = asset_ops.find_asset_by_barcode_and_mac(repository, barcode, mac_address)

    if not asset:
        return None

    # Update status in main table
    updated_asset = asset_ops.update_asset_status(
        repository, barcode, mac_address, AssetStatus.EXCESSED
    )

    # Also save to excess table for tracking
    if updated_asset:
        repository.save_to_excess(updated_asset)

    return updated_asset

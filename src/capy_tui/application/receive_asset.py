# asset_manager/workflows/receive_asset.py
from typing import Optional
from domain.asset import Asset
from infrastructure.sqlite_repository import SQLiteRepository
from domain import asset_ops


def receive_asset(
    repository: SQLiteRepository,
    barcode: str,
    mac_address: str,
) -> Optional[Asset]:
    """
    Receive an asset into the system.
    Returns the asset if successfully received, None if already exists.
    """
    # Normalize MAC address (remove separators)
    normalized_mac = mac_address.replace(":", "").replace("-", "")

    # Check if asset already exists
    existing_asset = asset_ops.find_asset_by_barcode_and_mac(
        repository, barcode, normalized_mac
    )

    if existing_asset:
        return None  # Asset already exists

    # Create new asset
    return asset_ops.create_asset(repository, barcode, normalized_mac)

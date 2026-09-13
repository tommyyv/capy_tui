# standard
from typing import List, Optional
from datetime import datetime

# framework

# user-defined
from .database import Database
from domain.asset import Asset, AssetStatus


class SQLiteRepository:
    """Repository for managing assets in SQLite database."""

    def __init__(self, database: Database):
        self.db = database

    def save(self, asset: Asset) -> Asset:
        """Save an asset to the database."""
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO assets (building, room, asset_tag, mac_address, status, created_timestamp, updated_timestamp)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
                (
                    asset.building,
                    asset.room,
                    asset.asset_tag,
                    asset.mac_address,
                    asset.status.value,
                    asset.created_timestamp.isoformat(),
                    asset.updated_timestamp.isoformat(),
                ),
            )
            conn.commit()
        return asset

    def save_to_excess(self, asset: Asset) -> Asset:
        """Save an asset to the excess table."""
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO excess_assets (building, room, asset_tag, mac_address, status, created_timestamp, updated_timestamp)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
                (
                    asset.building,
                    asset.room,
                    asset.asset_tag,
                    asset.mac_address,
                    asset.status.value,
                    asset.created_timestamp.isoformat(),
                    asset.updated_timestamp.isoformat(),
                ),
            )
            conn.commit()
        return asset

    def update(self, asset: Asset) -> Asset:
        """Update an existing asset."""
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                UPDATE assets
                SET status = ?, updated_timestamp = ?
                WHERE asset_tag = ? AND mac_address = ?
            """,
                (
                    asset.status.value,
                    asset.updated_timestamp.isoformat(),
                    asset.asset_tag,
                    asset.mac_address,
                ),
            )
            conn.commit()
        return asset

    def find_by_barcode_and_mac(
        self, asset_tag: str, mac_address: str
    ) -> Optional[Asset]:
        """Find an asset by asset_tag and MAC address."""
        result = self.db.execute_query(
            "SELECT * FROM assets WHERE asset_tag = ? AND mac_address = ?",
            (asset_tag, mac_address),
        )
        if result:
            row = result[0]
            return Asset(
                building=row["building"],
                room=row["room"],
                asset_tag=row["asset_tag"],
                mac_address=row["mac_address"],
                status=AssetStatus(row["status"]),
                created_timestamp=datetime.fromisoformat(row["created_timestamp"]),
                updated_timestamp=datetime.fromisoformat(row["updated_timestamp"]),
            )
        return None

    def get_all(self) -> List[Asset]:
        """Get all assets."""
        results = self.db.execute_query(
            "SELECT * FROM assets ORDER BY updated_timestamp DESC"
        )
        return [
            Asset(
                building=row["building"],
                room=row["room"],
                asset_tag=row["asset_tag"],
                mac_address=row["mac_address"],
                status=AssetStatus(row["status"]),
                created_timestamp=datetime.fromisoformat(row["created_timestamp"]),
                updated_timestamp=datetime.fromisoformat(row["updated_timestamp"]),
            )
            for row in results
        ]

    def get_all_excess(self) -> List[Asset]:
        """Get all excess assets."""
        results = self.db.execute_query(
            "SELECT * FROM excess_assets ORDER BY updated_timestamp DESC"
        )
        return [
            Asset(
                building=row["building"],
                room=row["room"],
                asset_tag=row["asset_tag"],
                mac_address=row["mac_address"],
                status=AssetStatus(row["status"]),
                created_timestamp=datetime.fromisoformat(row["created_timestamp"]),
                updated_timestamp=datetime.fromisoformat(row["updated_timestamp"]),
            )
            for row in results
        ]

    def delete_by_barcode_and_mac(self, asset_tag: str, mac_address: str) -> bool:
        """Delete an asset by barcode and MAC address."""
        count = self.db.execute_command(
            "DELETE FROM assets WHERE barcode = ? AND mac_address = ?",
            (asset_tag, mac_address),
        )
        return count > 0

    def delete_from_excess_by_barcode_and_mac(
        self, asset_tag: str, mac_address: str
    ) -> bool:
        """Delete an excess asset by barcode and MAC address."""
        count = self.db.execute_command(
            "DELETE FROM excess_assets WHERE asset_tag = ? AND mac_address = ?",
            (asset_tag, mac_address),
        )
        return count > 0

    def search(self, search_term: str) -> List[Asset]:
        """Search for assets by barcode or MAC address."""
        results = self.db.execute_query(
            """
            SELECT * FROM assets
            WHERE asset_tag LIKE ? OR mac_address LIKE ?
            ORDER BY updated_timestamp DESC
            """,
            (f"%{search_term}%", f"%{search_term}%"),
        )
        return [
            Asset(
                building=row["building"],
                room=row["room"],
                asset_tag=row["asset_tag"],
                mac_address=row["mac_address"],
                status=AssetStatus(row["status"]),
                created_timestamp=datetime.fromisoformat(row["created_timestamp"]),
                updated_timestamp=datetime.fromisoformat(row["updated_timestamp"]),
            )
            for row in results
        ]

    def search_excess(self, search_term: str) -> List[Asset]:
        """Search for excess assets by barcode or MAC address."""
        results = self.db.execute_query(
            """
            SELECT * FROM excess_assets
            WHERE asset_tag LIKE ? OR mac_address LIKE ?
            ORDER BY updated_timestamp DESC
            """,
            (f"%{search_term}%", f"%{search_term}%"),
        )
        return [
            Asset(
                building=row["building"],
                room=row["room"],
                asset_tag=row["asset_tag"],
                mac_address=row["mac_address"],
                status=AssetStatus(row["status"]),
                created_timestamp=datetime.fromisoformat(row["created_timestamp"]),
                updated_timestamp=datetime.fromisoformat(row["updated_timestamp"]),
            )
            for row in results
        ]

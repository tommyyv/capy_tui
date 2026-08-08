# standard
from dataclasses import dataclass, replace
from datetime import datetime
from enum import Enum
from typing import Optional

# framework

# user-defined


# TODO: add strip method that removes the first 5 characters when scanning the DOE.
class AssetStatus(Enum):
    ACTIVE = "Active"
    PENDING_EXCESS = "Pending Excess"
    IN_STOCK = "In-stock"
    EXCESS = "Excessed"


@dataclass(frozen=True)
class Asset:
    """Represents an asset in the system."""

    asset_tag: str
    status: AssetStatus
    created_timestamp: datetime
    updated_timestamp: datetime
    mac_address: Optional[str] = None
    building: Optional[str] = None
    room: Optional[str] = None

    def __post_init__(self) -> None:
        if self.mac_address is not None:
            if not self._is_valid_mac_address(self.mac_address):
                raise ValueError("Not a valid mac address.")

            normalized_mac = self._normalize_mac_address(self.mac_address)
            object.__setattr__(self, "mac_address", normalized_mac)

        if not self._is_valid_asset_tag(self.asset_tag):
            raise ValueError("Not a valid asset tag.")

    @staticmethod
    def _is_valid_asset_tag(asset_tag: str) -> bool:
        """Validate asset tag format.

        The length must be greater than 0.

        Returns a boolean.
        """
        return len(asset_tag.strip()) > 0

    @staticmethod
    def _is_valid_mac_address(mac: str) -> bool:
        """Validate MAC address format.

        Constraint:
            - MAC address must be equal to 12 characters. No more. No less.
            - MAC address must adhere to the hexdecimal system.

        Remove ".,-" characters and lower case the format

        Returns a boolean.
        """
        formatted_mac = mac.replace(":", "").replace("-", "").replace(".", "").lower()

        return len(formatted_mac) == 12 and all(
            c in "0123456789abcdefABCDEF" for c in formatted_mac
        )

    @staticmethod
    def _normalize_mac_address(mac: str) -> str:
        return mac.replace(":", "").replace("-", "").replace(".", "").lower()

    @classmethod
    def create_new(
        cls,
        asset_tag: str,
        mac_address: Optional[str],
        building: Optional[str],
        room: Optional[str],
    ) -> "Asset":
        """Create a new asset with current timestamps."""
        now = datetime.now()
        return cls(
            building=building,
            room=room,
            asset_tag=asset_tag,
            mac_address=mac_address,
            status=AssetStatus.IN_STOCK,
            created_timestamp=now,
            updated_timestamp=now,
        )

    def update_status(self, new_status: AssetStatus) -> "Asset":
        """Return a new asset with an updated status."""
        return replace(
            self,
            status=new_status,
            updated_timestamp=datetime.now(),
        )

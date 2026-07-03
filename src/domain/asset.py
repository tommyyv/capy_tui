# standard
from dataclasses import dataclass
from datetime import datetime
from enum import Enum

# framework

# user-defined


class AssetStatus(Enum):
    ACTIVE = "Active"
    PENDING_EXCESS = "Pending Excess"
    IN_STOCK = "In-stock"
    EXCESS = "Excessed"


@dataclass(frozen=True)
class Asset:
    """Represents an asset in the system."""

    barcode: str
    mac_address: str
    status: AssetStatus
    created_timestamp: datetime
    updated_timestamp: datetime

    @classmethod
    def create_new(cls, barcode: str, mac_address: str):
        """Create a new asset with current timestamps."""
        now = datetime.now()
        return cls(
            barcode=barcode,
            mac_address=mac_address.replace(":", "").replace("-", ""),
            status=AssetStatus.IN_STOCK,
            created_timestamp=now,
            updated_timestamp=now,
        )

    def update_status(self, new_status: AssetStatus):
        """Return a new asset with updated status."""
        return Asset(
            barcode=self.barcode,
            mac_address=self.mac_address,
            status=new_status,
            created_timestamp=self.created_timestamp,
            updated_timestamp=datetime.now(),
        )

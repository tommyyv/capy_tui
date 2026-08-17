# standard
import csv
from pathlib import Path
# framework

# user-defined
from domain.asset import Asset


class CSVService:
    """
    Static:
        - validate
        - normalize

    Public:
        - import
        - export
    """

    def read_csv(self, file_path: Path) -> list[dict[str, str | None]]:
        self._validate_csv(str(file_path))

        rows: list[dict[str, str | None]] = []

        with open(
            file_path,
            "r",
            newline="",
            encoding="utf-8",
        ) as file:
            reader = csv.DictReader(file)

            for row in reader:
                rows.append(self._normalize_row(row))

        return rows

    def export_csv(self, file: Path, assets: list[Asset]) -> Path:
        with open(file, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["building", "room", "asset_tag", "mac_address"])

            rows = [
                [asset.building, asset.room, asset.asset_tag, asset.mac_address]
                for asset in assets
            ]

            writer.writerows(rows)

        return Path(file)

    @staticmethod
    def _validate_csv(file_path: str) -> bool:
        path = Path(file_path)

        if not path.exists() or not path.is_file():
            print("path or file must exist")

        if path.suffix.lower() != ".csv":
            print("must be csv format")

        return True

    @staticmethod
    def _normalize_row(row: dict[str, str]) -> dict[str, str | None]:

        return {
            "building": row.get("building", "").strip(),
            "room": row.get("room", "").strip(),
            "asset_tag": row.get("asset_tag", "").strip(),
            "mac_address": row.get("mac_address", "")
            .strip()
            .replace(":", "")
            .replace("-", "")
            .replace(".", "")
            .upper()
            or None,
        }

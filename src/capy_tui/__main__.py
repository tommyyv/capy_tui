# standard
from pathlib import Path

# framework

# user-defined
from capy_tui.app import CapyTUI

DATABASE_PATH = Path("data") / "assets.db"
MOCK_DATABASE_PATH = Path("data/mock") / "mock_db.db"


def main() -> None:
    app = CapyTUI(db_path=MOCK_DATABASE_PATH)
    app.run()


if __name__ == "__main__":
    main()

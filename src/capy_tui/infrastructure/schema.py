# asset_manager/infrastructure/schema.py
SCHEMA_V1 = {
    "assets": """
        CREATE TABLE IF NOT EXISTS assets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            building TEXT,
            room TEXT,
            asset_tag TEXT NOT NULL,
            mac_address TEXT,
            status TEXT NOT NULL DEFAULT 'Active',
            created_timestamp TEXT NOT NULL,
            updated_timestamp TEXT NOT NULL,
            UNIQUE(asset_tag, mac_address)
        );
    """,
    "excess_assets": """
        CREATE TABLE IF NOT EXISTS excess_assets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            building TEXT,
            room TEXT,
            asset_tag TEXT NOT NULL,
            mac_address TEXT,
            status TEXT NOT NULL DEFAULT 'Excessed',
            created_timestamp TEXT NOT NULL,
            updated_timestamp TEXT NOT NULL,
            UNIQUE(asset_tag, mac_address)
        );
    """,
    "schema_versions": """
        CREATE TABLE IF NOT EXISTS schema_versions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            version TEXT NOT NULL,
            applied_at TEXT NOT NULL,
            UNIQUE(version)
        );
    """,
}

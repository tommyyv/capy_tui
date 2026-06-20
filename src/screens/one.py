# standard
import sqlite3
import pathlib
import csv
from typing import List, Tuple

# framework
from textual.app import ComposeResult
from textual.binding import Binding, BindingType
from textual.containers import (
    Horizontal,
    Vertical,
    VerticalScroll,
)
from textual import on
from textual.screen import Screen
from textual.widget import Widget
from textual.widgets import (
    DataTable,
    Input,
    Button,
)

# user-defined
import home


DATABASE_PATH = pathlib.Path().home() / "dev/infra/db/capy_tui/in_memory.db"


class Database:
    def __init__(self, db_path=DATABASE_PATH):
        self.db_conn = sqlite3.connect(db_path)
        self.conn_cursor = self.db_conn.cursor()
        self._create_inv_table()

    def _create_inv_table(self) -> None:
        query = """
            CREATE TABLE IF NOT EXISTS test_db (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                doe TEXT NOT NULL,
                mac_address TEXT NOT NULL
                );
            """

        self.run_query(query)

    def add_inv_item(self, barcode: str, mac_address: str) -> None:
        self.run_query(
            "INSERT INTO test_db (doe, mac_address) VALUES (?, ?);",
            barcode,
            mac_address,
        )

    def fetch_item_by_id(self, doe: str) -> List[Tuple[int, str]]:
        print(f"fetching item by doe: {doe}")
        return self.run_query("SELECT * from test_db WHERE doe = ?;", doe).fetchall()

    # [(int, str)] => [(id, doe), (id, doe),...]
    def fetch_all_items(self) -> List[Tuple[int, str]]:
        query = "SELECT * FROM test_db;"
        return self.run_query(query).fetchall()

    # TODO: fix functionality...should update the entry's doe, model, etc...where doe = MATCH
    def update_item(self, doe: str) -> None:
        self.run_query("UPDATE test_db SET name = ? WHERE doe = ?;", doe)
        # self.conn_cursor.execute(
        #     "UPDATE test_db SET name = ? WHERE doe = ?", ("new device 3", doe)
        # )

    def delete_item(self, doe: str) -> None:
        self.run_query("DELETE FROM test_db WHERE doe = ?;", doe)

    def clear_db(self):
        # TODO: fix reset autokey
        self.run_query("DELETE FROM test_db;")

    def export_to_csv(self):
        """
        1. connect to db, if havent already (done)
        2. grab headers (eh)
        3. fetch rows (eh)
        4. write to csv (eh)
        5. save csv file with current timestamp (not done)
        6. close connection (eh)
        """
        # conn already done

        # header rows
        # NOTE: this works...now i need to fix the saved path
        project_root = pathlib.Path(__file__).resolve().parent.parent

        with open(
            f"{project_root}/data/data.csv", "w", newline="", encoding="utf-8"
        ) as f:
            writer = csv.writer(f)

            # Write column headers
            writer.writerow(
                [description[0] for description in self.conn_cursor.description]
            )

            # Write data rows
            writer.writerows(self.fetch_all_items())

        # NOTE: what file am i accessing???
        # csv_file should be a directory path => how would i make the csv create a new file everytime with the correct
        # timestamp?

    # def backup_db(src_path: str, dst_path: str):
    #     pass

    def run_query(self, query, *query_args):
        result = self.conn_cursor.execute(query, query_args)
        self.db_conn.commit()

        return result


class DatabaseWidget(Widget):
    DEFAULT_CSS = """
        #db-container {
            background: gray;
        }

    """

    def __init__(self, db):
        super().__init__()
        self.db = db

    def compose(self) -> ComposeResult:
        with Horizontal(id="db-container"):
            table = DataTable(id="inv_table")
            with VerticalScroll(id="dataview", classes="with-border"):
                yield table
            with Vertical(id="utility-controls", classes="with-border"):
                yield Input(id="barcode", placeholder="enter item...")
                yield Input(id="mac", placeholder="enter mac address")
                yield Button("ADD", id="add")
                yield Button("DELETE ID", id="delete_id")
                yield Button("CLEAR DATABASE", id="clear")
                yield Button("SEARCH ITEM", id="search")
                yield Button("EXPORT", id="export")
                yield Button("REFRESH", id="refresh")
                yield Button("GO BACK", id="go_back")

    def on_mount(self) -> None:
        self.table = self.query_one("#inv_table", DataTable)
        self.refresh_all_items()

    def refresh_table_callback(self, rows: List[Tuple[int, str, str]]) -> None:
        self.table.clear(columns=True)

        self.table.add_column("ID")
        self.table.add_column("DOE")
        self.table.add_column("MAC_ADDRESS")

        for row in rows:
            self.table.add_row(str(row[0]), row[1], row[2])

    def refresh_all_items(self) -> None:
        rows = self.db.fetch_all_items()
        self.refresh_table_callback(rows)

    @on(Input.Submitted, "#add")
    @on(Button.Pressed, "#add")
    def on_input_submitted(self) -> None:
        input_widget: Input = self.query_one(Input)
        mac_input: Input = self.query_one("#mac", Input)
        barcode: str = input_widget.value[5:]
        mac_address: str = mac_input.value

        if barcode and mac_address:
            self.db.add_inv_item(barcode, mac_address)
            input_widget.value = ""
            self.refresh_all_items()

    @on(Button.Pressed, "#delete_id")
    def on_cancel_button_event(self) -> None:
        input_widget: Input = self.query_one(Input)
        id: str = input_widget.value

        if id:
            self.db.delete_item(id)
            input_widget.value = ""
            self.refresh_all_items()

    @on(Button.Pressed, "#clear")
    def on_clear_button_event(self) -> None:
        self.db.clear_db()
        self.refresh_all_items()

    @on(Button.Pressed, "#search")
    def on_search_button_pressed(self) -> None:
        input_widget: Input = self.query_one(Input)
        item_id: str = input_widget.value
        if item_id:
            rows = self.db.fetch_item_by_id(item_id)

            self.refresh_table_callback(rows)

    @on(Button.Pressed, "#export")
    def on_export_csv(self) -> None:
        print("[TEST] export to csv [TEST]")
        self.db.export_to_csv()

    @on(Button.Pressed, "#refresh")
    def on_refresh(self) -> None:
        self.refresh_all_items()

    @on(Button.Pressed, "#go_back")
    def on_back_button_pressed(self) -> None:
        self.app.switch_screen(home.Home())


class One(Screen):
    BINDINGS: list[BindingType] = [
        Binding("up", "scroll_up", "Scroll Up", show=False),
        Binding("down", "scroll_down", "Scroll Down", show=False),
        Binding("left", "scroll_left", "Scroll Left", show=False),
        Binding("right", "scroll_right", "Scroll Right", show=False),
        Binding("home", "scroll_home", "Scroll Home", show=False),
        Binding("end", "scroll_end", "Scroll End", show=False),
        Binding("pageup", "page_up", "Page Up", show=False),
        Binding("pagedown", "page_down", "Page Down", show=False),
        Binding("ctrl+pageup", "page_left", "Page Left", show=False),
        Binding(
            "ctrl+pagedown",
            "page_right",
            "Page Right",
            show=False,
        ),
    ]

    DEFAULT_CSS = """
        #dataview {
            width: 2fr
        }

        #utility-controls {
            width: 1fr
        }

    """

    def compose(self) -> ComposeResult:
        with Horizontal():
            yield DatabaseWidget(db=Database())

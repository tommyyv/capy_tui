# standard
import sqlite3
from typing import List, Tuple, Optional

# framework
from textual.app import App, ComposeResult, Widget
from textual import on
from textual.containers import Horizontal, Vertical, Container
from textual.widgets import (
    Header,
    Footer,
    Static,
    Button,
    DataTable,
    Input,
    Label,
)

# user-defined
data = [
    ("1111111",),
    ("2222222",),
    ("3333333",),
    ("4444444",),
]
'''data model
id: PK
name: String
model: String
barcode: String
quantity: Integer
initial_entry: DateTime
last_updated: DateTime
'''
# TODO: refactor using @dataclass (__init__, __repr__, __eq__ auto-gen)

#################
# CLASS OBJECTS #
#################


class Database():
    # TODO: refactor public to non-public methods
    # NOTE: CRUD functions work, need to revise a few but overall, it works.
    def __init__(self):
        self.db_conn = sqlite3.connect("test.db")
        self.conn_cursor = self.db_conn.cursor()
        self.create_inv_table()

    def create_inv_table(self) -> None:
        # TODO: add model field -> model TEXT NOT NULL
        query = """
            CREATE TABLE IF NOT EXISTS test_db (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                doe TEXT NOT NULL
                );
            """

        self.run_query(query)

    def add_inv_item(self, barcode: str) -> None:
        self.run_query("INSERT INTO test_db (doe) VALUES (?);", barcode)

    def fetch_item_by_id(self, doe: str) -> None:
        print(f"getting item by {doe}: ", self.conn_cursor.execute(
            "SELECT * FROM test_db WHERE doe = ?", (doe,)).fetchone())

    # [(int, str)] => [(id, doe), (id, doe),...]
    def fetch_all_items(self) -> List[Tuple[int, str]]:
        query = "SELECT * FROM test_db;"
        return self.run_query(query).fetchall()

    # TODO: fix functionality...should update the entry's doe, model, etc...where doe = MATCH
    def update_item(self, doe: str) -> None:
        self.conn_cursor.execute(
            "UPDATE test_db SET name = ? WHERE doe = ?", ('new device 3', doe))

        self.conn.commit()

    def delete_item(self, doe: str) -> None:
        query = "DELETE FROM test_db WHERE doe = ?;", doe

        self.run_query(query)

    def clear_db(self):
        query = "DELETE FROM test_db;"

        self.run_query(query)

    def run_query(self, query, *query_args):
        result = self.conn_cursor.execute(query, query_args)
        self.db_conn.commit()
        return result

###########
# WIDGETS #
###########


class Sidebar(Vertical):
    def compose(self) -> ComposeResult:
        yield Button("inventory", id="btn-inventory", classes="sidebar_btn")
        yield Button("excess", id="btn-excess", classes="sidebar_btn")
        yield Button("report", id="btn-report", classes="sidebar_btn")


class InvMgntTableWidget(Vertical):
    db: Database
    table: DataTable

    def __init__(self, db: Database) -> None:
        super().__init__()
        self.db = db

    def compose(self) -> ComposeResult:
        yield BarcodeInputWidget(self.db)
        yield DataTable(id="inv_table")

    def on_mount(self) -> None:
        self.refresh_table()

    def refresh_table(self) -> None:
        table: DataTable = self.query_one("#inv_table", DataTable)
        table.clear(columns=True)

        rows: List[Tuple[int, str]] = self.db.fetch_all_items()

        table.add_columns("ID", "DOE")

        for row in rows:
            # List[Tuple[int, str]]
            table.add_row(str(row[0]), row[1])

# TODO(bug): input submission isn't updating the database


class BarcodeInputWidget(Vertical):
    # what do i need for this input widget?
    # 1. submit button
    # 2. input box with label
    db: Database

    def __init__(self, db: Database) -> None:
        super().__init__()
        self.db = db

    def compose(self) -> ComposeResult:
        yield Input(placeholder="DOE")
        yield Button("Submit")

    def on_mount(self) -> None:
        pass

    @on(Input.Submitted)
    @on(Button.Pressed)
    def on_input_submitted(self, db: Database) -> None:
        input: str = self.query_one(Input)
        barcode: str = input.value
        self.mount(Label(barcode))
        input.value = ""

        if barcode:
            self.db.add_inv_item(barcode)
            db.refresh_table()


########
# MAIN #
########
class CapyTUI(App):
    CSS_PATH = "main.tcss"
    BINDINGS = []
    db: Database
    # TODO: add database path global and pass into the class constructor

    def __init__(self):
        super().__init__()
        self.db = Database()

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        yield Sidebar(id="sidebar")
        yield Container(id="content")  # dynamic content area
        yield Footer()

    def on_mount(self) -> None:
        self.title = "CAPY TUI - INV MGNT"

    def on_button_pressed(self, event: Button.Pressed) -> None:
        content = self.query_one("#content", Container)
        content.remove_children()

        if event.button.id == "btn-inventory":
            # Inventory dashboard
            content.mount(Static("Inventory Dashboard", classes="title"))
            table_widget = InvMgntTableWidget(self.db)
            # barcode_widget = BarcodeInputWidget(self.db)
            #
            # content.mount(barcode_widget)
            content.mount(table_widget)

        elif event.button.id == "btn-excess":
            content.mount(Static("Excess Dashboard", classes="title"))
        elif event.button.id == "btn-report":
            content.mount(Static("Report Dashboard", classes="title"))


if __name__ == "__main__":
    CapyTUI().run()

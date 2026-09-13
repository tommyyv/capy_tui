from textual import on
from textual.screen import Screen
from textual.app import ComposeResult
from textual.widgets import DataTable, Header, Button


import home


class Reports(Screen):
    def __init__(self, repository, db_table: str) -> None:
        self.repo = repository
        self.table = db_table

    def compose(self) -> ComposeResult:
        yield Header()
        yield DataTable()
        yield Button("Go Back", id="go_back")

    async def on_mount(self) -> None:
        # create new db object
        self.db: Database
        # establish db_conn and get schema of the db_table

        # create a DataTable object and query the data columns into it
        table = self.query_one(DataTable)

        # set columns and rows
        # TODO: fix db scope; needs to be defined and initialized
        columns = self.db.get_table_columns(self.table)
        rows = self.db.get_table_data(self.table)
        # set the datatable's columns and rows with the db_table's columns and rows
        table.add_columns(*columns)
        for row in rows:
            # for each col in the columns, give me the row for that indexed column
            table.add_row(*[row[col] for col in columns])

    @on(Button.Pressed, "#go_back")
    def on_go_back_button_pressed(self) -> None:
        self.app.switch_screen(home.Home())

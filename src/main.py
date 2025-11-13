# standard
import sqlite3
import UUID

# framework
from textual.app import App, ComposeResult, on
from textual.widgets import (
    Header,
    Footer,
    DataTable,
    Button,
    Input
)

# user-defined
'''data model
id: PK
name: String
model: String
barcode: String
quantity: Integer
initial_entry: DateTime
last_updated: DateTime
'''


class CapyTui(App):
    CSS_PATH = "main.tcss"
    BINDINGS = []

    def compose(self) -> ComposeResult:
        # yield widgets
        pass

    def on_mount(self):
        # upon mounting the applicaton, do this
        self.title = "Inventory Management"
        pass

    def action_x(self):
        pass

    # @on(Button.Pressed, "#add")
    # def action_add(self):
    #     def check_contact(contact_data):
    #         if contact_data:
    #             self.db.add_contact(contact_data)
    #             id, *contact = self.db.get_last_contact()
    #             self.query_one(DataTable).add_row(*contact, key=id)
    #
    #     self.push_screen(InputDialog(), check_contact)

    def on_button_pressed(self, event: Button.Pressed) -> None:
        self.exit(event.button.id)

    def add_asset():
        pass

    def get_asset_by_id():
        pass

    def get_all_assets():
        pass

    def update_asset():
        pass

    def delete_asset():
        pass


'''
logic:
1. init a database object
2. check if table exists => this is a must because you dont want to delete the existing table...
3. if working with the actual model then create an Asset object for those interactions (creating an item, etc)
4.

'''


class Database:
    def create_database():
        # TODO: add ip:port of server hosting db
        conn = sqlite3.connect("test_inv.db")
        conn_cursor = conn.cursor
        # logic

        conn.commit()
        conn.close()


class Asset:
    # constructor
    # what do i want the constructor to look like when I create an instance
    def __init__(self, doe: str, host_name: str, model: str):
        self.doe = doe  # scanned from that physical system
        # should this be formatted to make a naming convention? for example, if Windows =>
        self.host_name = host_name
        # add: DW + doe = DW-doe, if Linux add: DL + doe = DL-doe
        # barcode is assigned as the model upon scanning or selecting the model type
        # for example, barcode generated for "model-aa-1000" is assigned to the asset's model variable upon scanning or
        # selecting the model's barcode
        self.model = model

    # setters and getters?


if __name__ == "__main__":
    app = CapyTui()
    app.run()

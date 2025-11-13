import sqlite3

conn = sqlite3.connect("test.db")
conn_cursor = conn.cursor()


def test_database():
    # use :memory: as connection for non-persistent data

    # create table
    create_table()

    # add item: works
    add_item()

    # get item by id: works
    search_item_by_unique_id(2)

    # get items: works
    fetch_all_items()

    # update item: works...update to reflect doe
    update_item(2)

    # delete item: works...update to reflect doe
    # delete_item(1)

    print(conn_cursor.execute("SELECT * FROM test").fetchall())
    # print(conn.total_changes)

    conn.commit()
    conn.close()


def create_table():
    conn_cursor.execute(
        "CREATE TABLE IF NOT EXISTS test (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, model TEXT)")


def add_item():
    conn_cursor.execute(
        "INSERT INTO test (name, model) VALUES (?, ?)", ('device 1',
                                                         'model_0001'))

    conn_cursor.execute(
        "INSERT INTO test (name, model) VALUES (?, ?)", ('device 2',
                                                         'model_0002'))


def search_item_by_unique_id(id):
    print(f"getting item by {id}: ", conn_cursor.execute(
        "SELECT * FROM test WHERE id = ?", (id,)).fetchone())


def fetch_all_items():
    print(conn_cursor.execute("SELECT * FROM test").fetchall())


def update_item(id):
    conn_cursor.execute(
        "UPDATE test SET name = ? WHERE id = ?", ('new device 3', id))


def delete_item(id):
    conn_cursor.execute("DELETE FROM test WHERE id = ?", (id,))


test_database()

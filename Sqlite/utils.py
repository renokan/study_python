"""Utilits for sqlite3."""

import sqlite3


def init_db(path_to_db, schema_db):
    try:
        connection = sqlite3.connect(path_to_db)
        connection.executescript(schema_db)
    except sqlite3.DatabaseError as err:
        return str(err)
    else:
        return True


def create_connection(path_to_db):
    return sqlite3.connect(path_to_db)


def old_insert_row_data(connection, query, data):
    try:
        with connection:
            connection.execute(query, data)
    except sqlite3.IntegrityError:
        return False
    else:
        return True


def insert_in_db(connection, query, data):
    try:
        connection.execute(query, data)
    except sqlite3.IntegrityError:
        return False
    else:
        return True


def get_from_db(connection, query, data=None):
    if data:
        return [row for row in connection.execute(query, data)]
    else:
        return [row for row in connection.execute(query)]

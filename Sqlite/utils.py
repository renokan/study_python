"""Utilits for sqlite3."""
import sqlite3


def create_connection(path_to_db, schema_db=None):
    connection = sqlite3.connect(path_to_db)
    if schema_db:
        connection.executescript(schema_db)
    return connection


def old_insert_row_data(connection, query, data):
    try:
        with connection:
            connection.execute(query, data)
    except sqlite3.IntegrityError:
        return False
    else:
        return True


def insert_row_data(connection, query, data):
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

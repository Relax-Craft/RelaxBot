import sqlite3


class SQLConnection:
    __connected = False

    def __new__(cls):
        if cls.__connected == False:
            cls.__connected = sqlite3.connect("db/sqlite3/db.db")

        return cls.__connected
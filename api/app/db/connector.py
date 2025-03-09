import sqlite3
from contextlib import contextmanager


class DatabaseConnector:
    """
    A class to manage connections to an SQLite database.

    This class provides a context manager to handle SQLite database connections efficiently. It allows
    you to easily establish a connection to the database and ensures proper cleanup by closing the
    connection after use.

    Attributes:
        path (str): The path to the SQLite database file. Defaults to `'database.db'`.

    Methods:
        __init__(path: str): Initializes the `DatabaseConnector` with the given database file path.
            If no path is provided, it defaults to `'database.db'`.
        get_connection(): A context manager that provides a connection to the SQLite database.
            It automatically closes the connection after the block of code using it is executed.

    Usage:
        The context manager can be used to manage the SQLite connection as follows:

        Example:
            from database_connector import DatabaseConnector

            db_connector = DatabaseConnector('my_database.db')

            with db_connector.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM users")
                results = cursor.fetchall()
                print(results)
    """

    path = None

    def __init__(self, path: str = 'database.db'):
        DatabaseConnector.path = path

    @contextmanager
    def get_connection():
        conn = sqlite3.connect(DatabaseConnector.path)
        try:
            yield conn
        finally:
            conn.close()


import sqlite3
from pathlib import Path


class DatabaseConnection:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.connection = None

        return cls._instance

    def get_connection(self):
        if self.connection is None:
            db_path = Path(__file__).with_name("tasks.db")

            self.connection = sqlite3.connect(db_path)
            self.connection.row_factory = sqlite3.Row

        return self.connection

    def close_connection(self):
        if self.connection is not None:
            self.connection.close()
            self.connection = None

    def initialize_database(self):
        connection = self.get_connection()

        with connection:
            connection.execute("""
                CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    description TEXT,
                    date TEXT,
                    time TEXT,
                    priority TEXT NOT NULL DEFAULT 'medium',
                    category TEXT NOT NULL DEFAULT 'other',
                    status TEXT NOT NULL DEFAULT 'pending',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)


database = DatabaseConnection()
database.initialize_database()
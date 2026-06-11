import sqlite3
from pathlib import Path


class DatabaseManager:

    def __init__(self):
        db_path = Path("data/knowledge_base.db")
        db_path.parent.mkdir(exist_ok=True)

        self.connection = sqlite3.connect(db_path)
        self.connection.row_factory = sqlite3.Row

        self.create_tables()

    def execute(self, query, params=()):
        cur = self.connection.cursor()
        cur.execute(query, params)
        self.connection.commit()
        return cur

    def fetch_one(self, query, params=()):
        cur = self.connection.cursor()
        cur.execute(query, params)
        return cur.fetchone()

    def fetch_all(self, query, params=()):
        cur = self.connection.cursor()
        cur.execute(query, params)
        return cur.fetchall()

    def create_tables(self):
        self.execute("""
        CREATE TABLE IF NOT EXISTS projects(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE,
            parent_id INTEGER
        )
        """)

        self.execute("""
        CREATE TABLE IF NOT EXISTS attributes(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            project_id INTEGER,
            name TEXT,
            value_type TEXT,
            fuzzy_type TEXT
        )
        """)

        self.execute("""
        CREATE TABLE IF NOT EXISTS attribute_values(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            attribute_id INTEGER,
            value TEXT
        )
        """)

        self.execute("""
        CREATE TABLE IF NOT EXISTS fuzzy_variables(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            attribute_id INTEGER,
            scale_name TEXT,
            min_value REAL,
            max_value REAL,
            step REAL
        )
        """)

        self.execute("""
        CREATE TABLE IF NOT EXISTS terms(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fuzzy_variable_id INTEGER,
            name TEXT
        )
        """)

        self.execute("""
        CREATE TABLE IF NOT EXISTS membership_functions(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            term_id INTEGER,
            a REAL, b REAL, c REAL, d REAL
        )
        """)

        self.execute("""
        CREATE TABLE IF NOT EXISTS rules(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            project_id INTEGER,
            name TEXT
        )
        """)

        self.execute("""
        CREATE TABLE IF NOT EXISTS conditions(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            rule_id INTEGER,
            attribute_id INTEGER,
            value TEXT,
            condition_type TEXT
        )
        """)

        self.execute("""
        CREATE TABLE IF NOT EXISTS explanations(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            rule_id INTEGER,
            explanation_text TEXT
        )
        """)
import sqlite3
from datetime import datetime

class Tracker:
    """
    Structured Memory (SQL).
    Tracks: Health stats, Financial balances, Tasks.
    """
    
    def __init__(self, db_path="tracker.db"):
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self._init_tables()

    def _init_tables(self):
        # Health Table
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS health_log (
            id INTEGER PRIMARY KEY,
            date TEXT,
            metric TEXT, 
            value REAL,
            note TEXT
        )''')
        
        # Tasks Table
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY,
            title TEXT,
            status TEXT,
            created_at TEXT
        )''')
        self.conn.commit()

    def log_health(self, metric: str, value: float, note: str = ""):
        self.cursor.execute(
            "INSERT INTO health_log (date, metric, value, note) VALUES (?, ?, ?, ?)",
            (datetime.now().isoformat(), metric, value, note)
        )
        self.conn.commit()

    def add_task(self, title: str):
        self.cursor.execute(
            "INSERT INTO tasks (title, status, created_at) VALUES (?, ?, ?)",
            (title, "PENDING", datetime.now().isoformat())
        )
        self.conn.commit()

    def get_pending_tasks(self):
        self.cursor.execute("SELECT id, title FROM tasks WHERE status = 'PENDING'")
        return self.cursor.fetchall()

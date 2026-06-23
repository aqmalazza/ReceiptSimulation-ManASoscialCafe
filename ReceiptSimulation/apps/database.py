try:
    import mysql.connector
except ImportError:  # pragma: no cover
    mysql = None
else:
    mysql = mysql.connector


class Database:
    def __init__(self, config: dict):
        self.config = config

    def connect(self):
        if mysql is None:
            raise RuntimeError("mysql-connector-python belum terpasang. Jalankan: pip install -r requirements.txt")
        return mysql.connect(**self.config)

    def fetch_all(self, query: str, params: tuple = ()) -> list[dict]:
        conn = self.connect()
        cursor = None
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(query, params)
            return cursor.fetchall()
        finally:
            if cursor:
                cursor.close()
            conn.close()

    def fetch_one(self, query: str, params: tuple = ()) -> dict | None:
        conn = self.connect()
        cursor = None
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(query, params)
            return cursor.fetchone()
        finally:
            if cursor:
                cursor.close()
            conn.close()

    def execute_transaction(self, statements: list[tuple[str, tuple]]):
        conn = self.connect()
        cursor = None
        try:
            cursor = conn.cursor()
            for query, params in statements:
                cursor.execute(query, params)
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            if cursor:
                cursor.close()
            conn.close()

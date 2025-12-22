# DB connection and basic query execution.
import psycopg2
from psycopg2.extras import RealDictCursor
from ..config import DB_CONFIG

class DatabaseConnection:
    def __init__(self):
        self.connection = None

    def connect(self):
        try:
            self.connection = psycopg2.connect(
                host=DB_CONFIG['host'],
                port=DB_CONFIG['port'],
                database=DB_CONFIG['database'],
                user=DB_CONFIG['user'],
                password=DB_CONFIG['password']
            )
        except Exception as e:
            print(f"Error connecting to database: {e}")
            raise

    def close(self):
        if self.connection:
            self.connection.close()

    def execute_query(self, query, params=None):
        try:
            cursor = self.connection.cursor(cursor_factory=RealDictCursor)
            cursor.execute(query, params)
            return cursor.fetchall()
        except Exception as e:
            print(f"Error executing query: {e}")
            raise
        finally:
            cursor.close()

    def execute_update(self, query, params=None):
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, params)
            self.connection.commit()
            return cursor.rowcount
        except Exception as e:
            self.connection.rollback()
            print(f"Error executing update: {e}")
            raise
        finally:
            cursor.close()

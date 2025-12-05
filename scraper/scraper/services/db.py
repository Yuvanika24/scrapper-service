# Low-level DB access

import psycopg2
from psycopg2.extras import RealDictCursor
from ..config import DB_CONFIG
from datetime import datetime


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
            print("Connected to PostgreSQL database")
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

#  SCRAPER-RELATED FUNCTIONS

def get_parameters_for_url(db, industry_module_url_id):  # (param_name + selectors + transformers) 
   
    query = """
    SELECT param_name, selectors, transformers 
    FROM url_parameters 
    WHERE industry_module_url_id = %s
    """
    rows = db.execute_query(query, (industry_module_url_id,))

    if not rows:
        return []

    params = []
    for row in rows:
        params.append({
            "param_name": row["param_name"],
            "selector": row["selectors"],
            "transformer": row["transformers"]
        })

    return params


def get_latest_dom_signature(db, industry_module_url_id):

    query = """
    SELECT signature FROM signatures
    WHERE industry_module_url_id = %s
    ORDER BY last_checked DESC
    LIMIT 1 """

    result = db.execute_query(query, (industry_module_url_id,))
    return result[0]["signature"] if result else None # list of dictionaries


def save_dom_signature(db, industry_module_url_id, signature):
    now = datetime.now()
    
    query = """
    INSERT INTO signatures (industry_module_url_id, signature, last_checked, last_updated)
    VALUES (%s, %s, %s, %s)
    ON CONFLICT (industry_module_url_id)
    DO UPDATE SET signature = EXCLUDED.signature, last_checked = EXCLUDED.last_checked;
    """
    
    db.execute_update(query, (industry_module_url_id, signature, now, now))


def get_all_industry_module_urls(db): # [industry name, module name, url, industry_module_url_id]

    query = """
    SELECT 
        imu.id AS industry_module_url_id,
        i.name AS industry_name,
        m.name AS module_name,
        u.url AS url
    FROM industry_module_urls imu
    JOIN industry_modules im ON imu.industry_module_id = im.id
    JOIN industries i ON im.industry_id = i.id
    JOIN modules m ON im.module_id = m.id
    JOIN urls u ON imu.url_id = u.id
    """

    return db.execute_query(query)

# High-level DB service for scraper application.

from .connection import DatabaseConnection
from .db import (
    get_urls_with_params,
    get_latest_dom_signature,
    save_dom_signature,
    update_last_checked
)
from collections import defaultdict
from datetime import datetime

class DBService:
    def __init__(self):
        self.db = DatabaseConnection()
        self.db.connect()

    def get_db_connection(self):
        return self.db

    # --- URLs with parameters ---
    def get_urls_with_params(self):
        rows = self.db.execute_query(get_urls_with_params())
        return self._group_params(rows)

    def _group_params(self, rows):
        url_map = {}
        params_map = defaultdict(list)
        for row in rows:
            url_id = row["industry_module_url_id"]
            if url_id not in url_map:
                url_map[url_id] = {
                    "url": row["url"],
                    "industry_name": row["industry_name"],
                    "module_name": row["module_name"]
                }
            if row["param_name"]:
                params_map[url_id].append({
                    "param_name": row["param_name"],
                    "css_path": row["css_path"],
                    "transformer": row["transformers"]
                })
        return url_map, params_map

    # --- Signature functions ---
    def get_latest_dom_signature(self, industry_module_url_id):
        result = self.db.execute_query(get_latest_dom_signature(), (industry_module_url_id,))
        return result[0]["signature"] if result else None

    def save_dom_signature(self, industry_module_url_id, signature):
        now = datetime.now()
        self.db.execute_update(save_dom_signature(), (industry_module_url_id, signature, now, now))

    def update_last_checked(self, industry_module_url_id):
        now = datetime.now()
        self.db.execute_update(update_last_checked(), (now, industry_module_url_id)) 

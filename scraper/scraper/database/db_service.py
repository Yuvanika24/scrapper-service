from .connection import DatabaseConnection
from .db import (
    get_urls_with_params,
    get_latest_dom_signature,
    save_dom_signature,
    update_last_checked,
    get_keywords_for_industry_module,
    get_industry_module_id,
    get_targetted_urls
)
from collections import defaultdict
from datetime import datetime
from scraper.utils.url_utils import normalize_url
from scraper.constants import CSS_PATH, INDUSTRY_MODULE_URL_ID, MODULE_NAME, PARAM_NAME, TRANSFORMER, URL, INDUSTRY_NAME

class DBService:
    def __init__(self):
        self.db = DatabaseConnection()
        self.db.connect()

    def get_db_connection(self):
        return self.db

    # --- fetch URLs with parameters ---

    def get_urls_with_params(self, industry, module):
        rows = self.db.execute_query(get_urls_with_params(), (industry, module))
        return self.group_params(rows)

    def group_params(self, rows):
        url_map = {}
        params_map = defaultdict(list)
        for row in rows:
            url_id = row[INDUSTRY_MODULE_URL_ID]
            if url_id not in url_map:
                url_map[url_id] = {
                    URL: row[URL],
                    INDUSTRY_NAME: row[INDUSTRY_NAME],
                    MODULE_NAME: row[MODULE_NAME]
                }
            if row[PARAM_NAME]:
                params_map[url_id].append({
                    PARAM_NAME: row[PARAM_NAME],
                    CSS_PATH: row[CSS_PATH],
                    TRANSFORMER: row["transformers"]
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

    # --- Keywords functions ---

    def get_keywords_for_industry_module(self, industry, module):
        industry_module_id = self.get_industry_module_id(industry, module)
        keywords = self.get_keywords(industry_module_id)
        return industry_module_id, keywords

    def get_industry_module_id(self, industry_name, module_name):
        result = self.db.execute_query(get_industry_module_id(), (industry_name, module_name))
        return result[0]["id"] if result else None
    
    def get_keywords(self, industry_module_id):
        rows = self.db.execute_query(get_keywords_for_industry_module(), (industry_module_id,))
        return [row["keyword"] for row in rows]

    # --- Normalized urls ---
    
    def get_targetted_urls(self, industry, module):
        rows = self.db.execute_query(get_targetted_urls(), (industry, module))

        return {
            normalize_url(row["url"])
            for row in rows
            if row.get("url")
        }



# High-level DB interface for the scraper

from .db import (
    DatabaseConnection,
    get_all_industry_module_urls,
    get_parameters_for_url
)

class DBService:
    def __init__(self):
        self.db = DatabaseConnection()
        self.db.connect()
        
    def get_db_connection(self):
        return self.db

    def get_url_configs(self):
        return get_all_industry_module_urls(self.db)

    def get_params(self, module_url_id):
        return get_parameters_for_url(self.db, module_url_id)

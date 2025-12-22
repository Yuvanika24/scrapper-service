
from scraper.database.db_service import DBService
from scraper.utils.url_utils import normalize_url
from scraper.constants import URL

class UrlDataService:
    _cache = {}  # class-level cache, keyed by industry+module

    def __init__(self, industry: str, module: str):
        self.industry = industry
        self.module = module
        self.db = DBService()

    def get_targeted_urls(self):
        key = f"{self.industry}_{self.module}"
        if key not in self._cache:
            url_map, params_map = self.db.get_urls_with_params()
            self._cache[key] = {
                "url_map": url_map,
                "params_map": params_map,
                "normalized_urls": {normalize_url(u[URL]) for u in url_map.values()}
            }
        return self._cache[key]

import scrapy, json
from scraper.services.database.db_service import DBService
from scraper.services.signature_service import SignatureService
from scraper.items import TargettedScrapedItem
from scraper.constants import INDUSTRY_URL_ID, INDUSTRY_NAME, MODULE_NAME, PARAMETER_CONFIGS, URL, SCRAPED_DATA, HEADERS
from scraper.transformers.transformers import TRANSFORMER_FUNCTIONS

class TargettedSpider(scrapy.Spider):
    name = "targetted_spider"

    custom_settings = {
        "FEEDS": {
            "output/targetted.json": {
                "format": "json",
                "encoding": "utf8",
                "indent": 4,
            }
        }
    }

    def start_requests(self):
        print("Start Targetted Spider requests")

        self.db_service = DBService()
        self.signature_service = SignatureService(self.db_service)

        url_map, params_map = self.db_service.get_urls_with_params()

        # Yield all URLs
        for url_id, url_data in url_map.items():
            yield scrapy.Request(
                url=url_data["url"],
                meta={
                    INDUSTRY_URL_ID: url_id,
                    INDUSTRY_NAME: url_data[INDUSTRY_NAME],
                    MODULE_NAME: url_data[MODULE_NAME],
                    PARAMETER_CONFIGS: params_map[url_id]
                },
                callback=self.parse,
                headers=HEADERS,
                dont_filter=True
            )

    def parse(self, response):
        print("Parsing response for URL:", response.url)

        params = response.meta[PARAMETER_CONFIGS]
        industry_module_url_id = response.meta[INDUSTRY_URL_ID]
        industry_name = response.meta[INDUSTRY_NAME]
        module_name = response.meta[MODULE_NAME]

        # Mini DOM + signature
        mini_dom = self.signature_service.build_mini_dom(response, params)
        new_signature = self.signature_service.calculate_signature(mini_dom)

        dom_changed = self.signature_service.compare_and_update(industry_module_url_id, new_signature)
        print("DOM Changed:", dom_changed)
        if dom_changed:
            self.logger.info(f"DOM changed for URL ID {industry_module_url_id}. Skipping scrape.")
            return

        self.logger.info(f"Scraping URL ID {industry_module_url_id} (new run or unchanged DOM)")

        # Extract & transform data
        processed_data = {}

        for param in params:
            selector = param.get("css_path")
            raw_html = None

            if selector:
                # XPath selector
                if selector.startswith("//"):
                    raw_html = response.xpath(selector).get()
                # CSS selector
                else:
                    raw_html = response.css(selector).xpath("string()").get()

            if raw_html:
                raw_html = raw_html.strip()
            transformer_string = param.get("transformer")
            processed_data[param['param_name']] = self.apply_transformers(
                raw_html, transformer_string
            )

        print(json.dumps(processed_data, indent=2, ensure_ascii=False))

        # Yield item
        item = TargettedScrapedItem()
        item[INDUSTRY_NAME] = industry_name
        item[MODULE_NAME] = module_name
        item[URL] = response.url
        item[SCRAPED_DATA] = processed_data
        yield item

    def apply_transformers(self, value, transformer_string):
        if not transformer_string:
            return value
        for t in [t.strip() for t in transformer_string.split(",")]:
            func = TRANSFORMER_FUNCTIONS.get(t)
            if func:
                try:
                    value = func(value)
                except Exception as e:
                    self.logger.error(f"Transformer {t} failed: {e}")
        return value

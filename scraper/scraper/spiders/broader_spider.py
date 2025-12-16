import scrapy, json
from scraper.items import BroaderScrapedItem
from scraper.services.database.db_service import DBService
from scraper.services.cse_service import get_cse_results
from scraper.services.xpath_extractor import scrape_page_with_xpath
from scraper.constants import HEADERS, INDUSTRY_MODULE_ID, INDUSTRY_NAME, MODULE_NAME, URL, KEYWORD, XPATH, CONTENT, SOURCE

class BroaderSpider(scrapy.Spider):
    name = "broader_spider"

    custom_settings = {
        "FEEDS": {
            "output/broader.json": {
                "format": "json",
                "encoding": "utf8",
                "indent": 4,
            }
        }
    }

    def __init__(self, industry=None, module=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.industry = industry
        self.module = module
        self.db_service = DBService()

    def start_requests(self):
        print("Start Broader Spider requests")

        #single call
        industry_module_id = self.db_service.get_industry_module_id(self.industry, self.module)
        keywords = self.db_service.get_keywords(industry_module_id)

        print(f"Keywords for Industry: {self.industry}, Module: {self.module}")
        print("industry_module_id:", industry_module_id)

        # total_items = 0
        # MAX_ITEMS = 2  # total requests across all keywords

        for keyword in keywords:
            try:
                links = get_cse_results(keyword)
            except Exception as e:
                self.logger.error(f"CSE failed for {keyword}: {e}")
                continue

            for url in links:
                # if total_items >= MAX_ITEMS:
                #     return
                # total_items += 1

                yield scrapy.Request(
                    url=url,
                    meta={"keyword": keyword, "industry_module_id": industry_module_id},
                    callback=self.parse,
                    headers=HEADERS,
                    dont_filter=True
                )

    def parse(self, response):
        keyword = response.meta["keyword"]
        industry_module_id = response.meta["industry_module_id"]

        results = scrape_page_with_xpath(response.url, keyword)

        print(json.dumps(results, indent=2, ensure_ascii=False))

        for res in results:
            item = BroaderScrapedItem()
            item[INDUSTRY_NAME] = self.industry
            item[MODULE_NAME] = self.module
            item[INDUSTRY_MODULE_ID] = industry_module_id
            item[SOURCE] = "untrusted"
            item[URL] = res["url"]
            item[KEYWORD] = res["keyword"]
            item[XPATH] = res["xpath"]
            item[CONTENT] = res["content"]

            yield item

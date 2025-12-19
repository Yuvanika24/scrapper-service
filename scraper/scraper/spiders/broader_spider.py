import scrapy, json
from scraper.items import BroaderScrapedItem
from scraper.services.database.db_service import DBService
from scraper.services.cse_service import get_cse_results
from scraper.services.xpath_extractor import scrape_page_with_xpath
from scraper.utils.url_utils import normalize_url
from scraper.constants import HEADERS, INDUSTRY_MODULE_ID, INDUSTRY_NAME, MODULE_NAME, URL, KEYWORD, XPATH, CONTENT, SOURCE

class BroaderSpider(scrapy.Spider):
    name = "broader_spider"

    custom_settings = {
        "FEEDS": {
            "output/broader.json": {
                "format": "json",
                "encoding": "utf8",
                "indent": 4,
                "overwrite": True
            }
        }
    }

    def __init__(self, industry=None, module=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.industry = industry
        self.module = module
        self.db_service = DBService()

        targeted_urls = self.db_service.get_all_targetted_urls()
        self.targeted_url_set = set(targeted_urls)

        self.logger.info("Loaded %d targeted URLs for dedup",len(self.targeted_url_set))

    def start_requests(self):
        print("Start Broader Spider requests")

        industry_module_id, keywords = self.db_service.get_keywords_for_industry_module(
            self.industry,
            self.module
        )

        print(f"Keywords for Industry: {self.industry}, Module: {self.module}")
        print("industry_module_id:", industry_module_id)

        # static_urls = [
        #     "https://www.grandviewresearch.com/industry-analysis/solar-panels-market",
        #     "https://www.precedenceresearch.com/solar-pv-panels-market",
        #     "https://www.marketresearchfuture.com/reports/solar-panel-market-3147",
        #     "https://www.fortunebusinessinsights.com/solar-panel-market-102888",
        #     "https://www.alliedmarketresearch.com/solar-panel-market"
        # ]

        for keyword in keywords:
            try:
                links = get_cse_results(keyword)
            except Exception as e:
                self.logger.error(f"CSE failed for {keyword}: {e}")
                continue

            for url in links:
            #for url in static_urls:
                norm_url = normalize_url(url)

                if norm_url in self.targeted_url_set:
                    self.logger.info(
                        "Skipping CSE URL (already targeted): %s",
                        norm_url
                    )
                    continue
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

        print("response:", response)

        results = scrape_page_with_xpath(response, keyword)

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

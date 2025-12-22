import scrapy, json
from scraper.items import BroaderScrapedItem
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
                "overwrite": True
            }
        }
    }

    def __init__(self, jobs=None, industry=None, module=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.industry = industry
        self.module = module
        self.jobs = jobs or []

    def start_requests(self):
        print("Starting Broader Spider requests")

        for job in self.jobs:
            yield scrapy.Request(
                url=job.url,
                headers=HEADERS,
                dont_filter=True,
                callback=self.parse,
                meta={
                    KEYWORD: job.keyword,
                    INDUSTRY_MODULE_ID: job.industry_module_id,
                }
            )

    def parse(self, response):
        keyword = response.meta[KEYWORD]
        industry_module_id = response.meta[INDUSTRY_MODULE_ID]

        results = scrape_page_with_xpath(response, keyword)

        #print(json.dumps(results, indent=2, ensure_ascii=False))

        for res in results:
            item = BroaderScrapedItem()
            item[INDUSTRY_NAME] = self.industry
            item[MODULE_NAME] = self.module
            item[INDUSTRY_MODULE_ID] = industry_module_id
            item[SOURCE] = "untrusted" # temporary
            item[URL] = res[URL]
            item[KEYWORD] = res[KEYWORD]
            item[XPATH] = res[XPATH]
            item[CONTENT] = res[CONTENT]

            yield item

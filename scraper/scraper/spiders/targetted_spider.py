import scrapy
from scraper.items import TargettedScrapedItem
from scraper.utils.transformers import TRANSFORMER_FUNCTIONS
from scraper.constants import INDUSTRY_MODULE_URL_ID, INDUSTRY_NAME, MODULE_NAME, PARAMETER_CONFIGS, URL, SCRAPED_DATA, HEADERS

class TargettedSpider(scrapy.Spider):
    name = "targetted_spider"

    custom_settings = {
        "FEEDS": {
            "output/targetted.json": {
                "format": "json",
                "encoding": "utf8",
                "indent": 4,
                "overwrite": True
            }
        }
    }

    def __init__(self, jobs=None, signature_service=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.jobs = jobs or []
        self.signature_service = signature_service

    def start_requests(self):
        print("Starting target spider requests")

        for job in self.jobs:
            # Yield all URLs
            yield scrapy.Request(
                url=job.url,
                headers=HEADERS,
                dont_filter=True,
                callback=self.parse,
                meta={
                    INDUSTRY_MODULE_URL_ID: job.industry_module_url_id,
                    INDUSTRY_NAME: job.industry_name,
                    MODULE_NAME: job.module_name,
                    PARAMETER_CONFIGS: job.params
                }
            )

    def parse(self, response):

        params = response.meta[PARAMETER_CONFIGS]
        industry_module_url_id = response.meta[INDUSTRY_MODULE_URL_ID]
        industry_name = response.meta[INDUSTRY_NAME]
        module_name = response.meta[MODULE_NAME]

        # Mini DOM + signature
        if self.signature_service:
            mini_dom = self.signature_service.build_mini_dom(response, params)
            new_signature = self.signature_service.calculate_signature(mini_dom)

            dom_changed = self.signature_service.compare_and_update(
                industry_module_url_id,
                new_signature
            )

            if dom_changed:
                self.logger.info(f"DOM changed for URL ID {industry_module_url_id}. Skipping scrape.")
                return

        processed_data = {}

        for param in params:
            selector = param.css_path
            raw_html = None

            if selector:
                selector = selector.strip()
                is_xpath = selector.startswith("//") or selector.startswith("(")

                if "/@" in selector:
                    raw_html = ",".join(
                        response.xpath(selector).getall()
                        if is_xpath else response.css(selector).getall()
                    )
                else:
                    nodes = response.xpath(selector) if is_xpath else response.css(selector)
                    texts = nodes.xpath(".//text()").getall()
                    raw_html = " ".join(t.strip() for t in texts if t.strip())

            if raw_html:
                raw_html = raw_html.strip()
                if raw_html.startswith("/"):
                    raw_html = response.urljoin(raw_html)

            processed_data[param.param_name] = self.apply_transformers(
                raw_html, param.transformer)

        processed_data = dict(sorted(processed_data.items()))

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

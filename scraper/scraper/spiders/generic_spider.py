import scrapy, json
from scraper.services.db_service import DBService
from scraper.transformers.transformers import TRANSFORMER_FUNCTIONS
from scraper.services.signature_service import SignatureService
from scraper.items import GenericScrapedItem


class GenericSpider(scrapy.Spider):
    name = "generic_spider"

    def start_requests(self):
        self.db_service = DBService()
        self.signature_service = SignatureService(self.db_service.get_db_connection())

        urls_data = self.db_service.get_url_configs()

        for data in urls_data:
            module_url_id = data.get('industry_module_url_id')
            if not module_url_id:
                raise ValueError(f"URL data missing ID field: {data}")

            params = self.db_service.get_params(module_url_id)

            yield scrapy.Request(
                url=data['url'],
                meta={
                    "industry_module_url_id": module_url_id,
                    "industry_name": data.get("industry_name"),
                    "module_name": data.get("module_name"),
                    "params": params
                }
            )

    def parse(self, response):
        params = response.meta['params']
        industry_module_url_id = response.meta['industry_module_url_id']
        industry_name = response.meta['industry_name']
        module_name = response.meta['module_name']

        # Mini DOM + signature
        mini_dom = self.signature_service.build_mini_dom(response, params)
        new_signature = self.signature_service.calculate_signature(mini_dom)

        # Skip scraping if DOM changed
        dom_changed = self.signature_service.compare_and_update(
            industry_module_url_id,
            new_signature
        )
        if dom_changed:
            self.logger.info(f"DOM changed for URL ID {industry_module_url_id}. Skipping scrape.")
            return

        self.logger.info(f"Scraping URL ID {industry_module_url_id} (new run or unchanged DOM)")

        # Extract & transform data
        processed_data = {}
        for param in params:
            selector = param.get("selectors") or param.get("selector")
            raw_html = response.css(selector).xpath("string()").get()
            if raw_html:
                raw_html = raw_html.strip()

            transformer_string = param.get("transformer")
            processed_data[param['param_name']] = self.apply_transformers(raw_html, transformer_string)

        print(json.dumps(processed_data, indent=2, ensure_ascii=False))

        # Yield an Item
        item = GenericScrapedItem()
        item['industry_name'] = industry_name
        item['module_name'] = module_name
        item['url'] = response.url
        item['scraped_data'] = processed_data

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

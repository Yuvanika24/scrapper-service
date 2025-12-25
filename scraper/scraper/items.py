import scrapy

class TargettedScrapedItem(scrapy.Item):
    industry_name = scrapy.Field()
    module_name = scrapy.Field()
    url = scrapy.Field()
    scraped_data = scrapy.Field()
    image_urls = scrapy.Field()

class BroaderScrapedItem(scrapy.Item):
    industry_name = scrapy.Field()
    module_name = scrapy.Field()
    industry_module_id = scrapy.Field()
    source = scrapy.Field()               
    url = scrapy.Field()
    keyword = scrapy.Field()
    xpath = scrapy.Field()
    content = scrapy.Field()
    match_count = scrapy.Field()  # for debugging
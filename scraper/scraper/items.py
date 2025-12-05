import scrapy

class GenericScrapedItem(scrapy.Item):
    industry_name = scrapy.Field()
    module_name = scrapy.Field()
    url = scrapy.Field()
    scraped_data = scrapy.Field()

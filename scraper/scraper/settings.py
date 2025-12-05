# Scrapy settings for scraper project

BOT_NAME = "scraper"

# Modules where Scrapy will look for spiders
SPIDER_MODULES = ["scraper.spiders"]
NEWSPIDER_MODULE = "scraper.spiders"

# Control Logging
LOG_LEVEL = 'ERROR'
TELNETCONSOLE_ENABLED = False

# Respect robots.txt rules
ROBOTSTXT_OBEY = True

# Feed export settings (for JSON/CSV output)
FEED_EXPORT_ENCODING = "utf-8"

# Future-proof settings 
REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"

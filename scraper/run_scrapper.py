from scrapy.crawler import CrawlerProcess
from scraper.spiders.generic_spider import GenericSpider

def main():
    print("Choose Industry:")
    print("1. Solar")
    print("2. Semiconductor")
    
    industry_choice = input("Enter choice: ")
    if industry_choice == "1":
        industry = "Solar"
    elif industry_choice == "2":
        industry = "Semiconductor"
    else:
        print("Invalid choice. Exiting.")
        return

    print("\nChoose Module:")
    print("1. Market Analysis")
    print("2. Competitor Analysis")
    
    module_choice = input("Enter choice: ")
    if module_choice == "1":
        module = "Market Analysis"
    elif module_choice == "2":
        module = "Competitor Analysis"
    else:
        print("Invalid choice. Exiting.")
        return

    # Only mapped combination: Solar + Market Analysis
    if industry_choice == "1" and module_choice == "1":
        print("\nRunning Solar Market Analysis...\n")

        # Run existing spider
        process = CrawlerProcess({
            'FEEDS': {
                'output.json': {'format': 'json', 'encoding': 'utf8'}
            },
            'LOG_LEVEL': 'ERROR',
            'TELNETCONSOLE_ENABLED': False
        })
        process.crawl(GenericSpider)
        process.start()
    else:
        print(f"\nNo logic mapped for Industry: {industry}, Module: {module} yet.")
        print("Exiting.")

if __name__ == "__main__":
    main()

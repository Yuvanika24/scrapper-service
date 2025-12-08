from scrapy.crawler import CrawlerProcess
from scraper.spiders.generic_spider import GenericSpider
from scrapy.utils.project import get_project_settings

def main():
    print("Choose Industry:\n1. Solar\n2. Semiconductor")
    industry_choice = input("Enter choice: ")

    match industry_choice:
        case "1":
            industry = "Solar"
        case "2":
            industry = "Semiconductor"
        case _:
            print("Invalid choice. Exiting.")
            return

    print("\nChoose Module:\n1. Market Analysis\n2. Competitor Analysis")
    module_choice = input("Enter choice: ")

    match module_choice:
        case "1":
            module = "Market Analysis"
        case "2":
            module = "Competitor Analysis"
        case _:
            print("Invalid choice. Exiting.")
            return

    match (industry, module):
        case ("Solar", "Market Analysis"):
            print(f"\nRunning {industry} - {module}...\n")
            process = CrawlerProcess(get_project_settings())
            process.crawl(GenericSpider)
            process.start()
        case _:
            print(f"\nNo logic mapped for Industry: {industry}, Module: {module} yet. Exiting.")

if __name__ == "__main__":
    main()

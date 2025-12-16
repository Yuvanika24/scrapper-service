from scrapy.crawler import CrawlerProcess
from scraper.spiders.targetted_spider import TargettedSpider
from scraper.spiders.broader_spider import BroaderSpider
from scrapy.utils.project import get_project_settings

def main():
    print("Choose Industry:\n1. Solar Panel\n2. Semiconductor")
    industry_choice = input("Enter choice: ")

    match industry_choice:
        case "1":
            industry = "Solar Panel"
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


    if industry == "Solar Panel" and module == "Market Analysis":
        
        settings = get_project_settings()

        process = CrawlerProcess(settings)
        process.crawl(TargettedSpider)
        process.crawl(BroaderSpider, industry=industry, module=module)
        process.start()

    else:
        print(f"No logic mapped for Industry: {industry}, Module: {module} yet. Exiting.")

if __name__ == "__main__":
    main()


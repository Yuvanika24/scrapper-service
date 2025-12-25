from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from scraper.spiders.targetted_spider import TargettedSpider
from scraper.spiders.broader_spider import BroaderSpider

from scraper.job_builder.targetted_job_builder import TargettedJobBuilder
from scraper.job_builder.broader_job_builder import BroaderJobBuilder

from scraper.database.db_service import DBService
from scraper.services.signature_service import SignatureService

def main():
    print("Choose Industry:\n1. Solar Panel\n2. Semiconductor\n3. Battery")
    industry_choice = input("Enter choice: ")

    match industry_choice:
        case "1":
            industry = "Solar Panel"
        case "2":
            industry = "Semiconductor"
        case "3":
            industry = "Battery"
        case _:
            print("Invalid choice.")
            return

    print("\nChoose Module:\n1. Market Analysis\n2. Competitor Analysis\n3. Market Feasibilty\n4. Technical Implementation\n5. Compliance & Safety")
    module_choice = input("Enter choice: ")

    match module_choice:
        case "1":
            module = "Market Analysis"
        case "2":
            module = "Competitor Analysis"
        case "3":
            module = "Market Feasibilty"
        case "4":
            module = "Technical Implementation"
        case "5":
            module = "Compliance Safety"
        case _:
            print("Invalid choice.")
            return

    settings = get_project_settings()
    process = CrawlerProcess(settings)

    db_service = DBService()
    signature_service = SignatureService(db_service)

    # Targetted
    targetted_jobs = TargettedJobBuilder(industry=industry, module=module).build()
    process.crawl(TargettedSpider, jobs=targetted_jobs, signature_service=signature_service)

    # Broader
    broader_jobs = BroaderJobBuilder(industry=industry, module=module).build()
    process.crawl(BroaderSpider, jobs=broader_jobs, industry=industry, module=module)

    process.start()

if __name__ == "__main__":
    main()

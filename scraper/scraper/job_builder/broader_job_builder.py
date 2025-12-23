import logging
from scraper.dto.broader_dto import BroaderJob
from scraper.services.targetted_url_provider_service import UrlDataService
from scraper.services.cse_service import get_cse_results
from scraper.utils.url_utils import normalize_url

logger = logging.getLogger(__name__)


class BroaderJobBuilder:
    def __init__(self, industry: str, module: str):
        self.industry = industry
        self.module = module
        self.job_data_service = UrlDataService(industry, module)

    def build(self) -> list[BroaderJob]:
        jobs = []

        industry_module_id, keywords = (
            self.job_data_service.db.get_keywords_for_industry_module(
                self.industry,
                self.module
            )
        )
        # Get targeted URLs from cache
        data = self.job_data_service.get_targeted_urls()
        targeted_url_set = data["normalized_urls"]

        for keyword in keywords:
            try:
                links = get_cse_results(keyword)
            except Exception as e:
                logger.error("CSE failed for keyword '%s': %s", keyword, e)
                continue

            for url in links:
                norm_url = normalize_url(url)
                if norm_url in targeted_url_set:
                    continue

                jobs.append(
                    BroaderJob(
                        industry=self.industry,
                        module=self.module,
                        industry_module_id=industry_module_id,
                        keyword=keyword,
                        url=url,
                    )
                )

        return jobs

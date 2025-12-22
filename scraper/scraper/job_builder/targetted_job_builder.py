from scraper.dto.targetted_dto import TargettedJob, TargettedParamConfig
from scraper.constants import CSS_PATH, INDUSTRY_NAME, MODULE_NAME, PARAM_NAME, TRANSFORMER, URL
from scraper.services.targetted_url_provider_service import UrlDataService

class TargettedJobBuilder:
    def __init__(self, industry: str, module: str):
        self.industry = industry
        self.module = module
        self.job_data_service = UrlDataService(industry, module)
    
    def build(self) -> list[TargettedJob]:
        jobs = []
        data = self.job_data_service.get_targeted_urls()
        url_map, params_map = data["url_map"], data["params_map"]

        for url_id, url_data in url_map.items():
            raw_params = params_map.get(url_id, [])
            param_configs = [
                TargettedParamConfig(
                    param_name = p[PARAM_NAME],
                    css_path = p.get(CSS_PATH),
                    transformer = p.get(TRANSFORMER),
                )
                for p in raw_params
            ]
            jobs.append(
                TargettedJob(
                    industry_module_url_id=url_id,
                    industry_name=url_data[INDUSTRY_NAME],
                    module_name=url_data[MODULE_NAME],
                    url=url_data[URL],
                    params=param_configs
                )
            )
        return jobs

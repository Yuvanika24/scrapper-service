
from dataclasses import dataclass, field
from typing import List

@dataclass
class TargettedParamConfig:
    param_name: str
    css_path: str
    transformer: str

@dataclass
class TargettedJob:
    industry_module_url_id: int
    industry_name: str
    module_name: str
    url: str
    params: List[TargettedParamConfig] = field(default_factory=list)

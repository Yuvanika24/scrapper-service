import json
import hashlib
from scraper.services.database.db_service import DBService

class SignatureService:
    def __init__(self, db_service: DBService):
        self.db_service = db_service

    def build_mini_dom(self, response, params):
        mini_dom = {}

        for param in params:
            selector = param.get("css_path")
#           Debugging output
#             if selector:
#                 print("Selector:", selector)
#                 sel = selector.strip()
#                 is_xpath = sel.startswith("//") or sel.startswith("(")

#                 print(
#                     "Matches count:",
#                     len(response.xpath(sel)) if is_xpath else len(response.css(sel))
# )
            if not selector:
                continue
            try:
                if selector.strip().startswith("//"):
                    selected_elements = response.xpath(selector)
                else:
                    selected_elements = response.css(selector)

                tags = [el.root.tag for el in selected_elements] if selected_elements else []

                mini_dom[param['param_name']] = {
                    "selector": selector,
                    "count": len(selected_elements),
                    "tags": tags
                }
            except Exception as e:
                mini_dom[param['param_name']] = {
                    "selector": selector,
                    "count": 0,
                    "tags": [],
                    "error": str(e)
                }
        return mini_dom

    def calculate_signature(self, mini_dom):
        serialized = json.dumps(mini_dom, sort_keys=True, ensure_ascii=False)
        return hashlib.sha256(serialized.encode()).hexdigest()
        
    def compare_and_update(self, industry_module_url_id, new_signature):
        old_signature = self.db_service.get_latest_dom_signature(industry_module_url_id)

        # first entry
        if old_signature is None:
            self.db_service.save_dom_signature(industry_module_url_id, new_signature)
            return False  # No change

        # susequent runs
        if old_signature != new_signature:
            self.db_service.save_dom_signature(industry_module_url_id, new_signature)
            return True  # DOM changed

        # same signature
        self.db_service.update_last_checked(industry_module_url_id)
        return False  # No change


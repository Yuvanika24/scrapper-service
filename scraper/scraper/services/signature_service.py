import json
import hashlib
from .db import get_latest_dom_signature, save_dom_signature

class SignatureService:
    def __init__(self, db):
        self.db = db

    def build_mini_dom(self, response, params):
        mini_dom = {}
        for param in params:
            selector = param.get("selector")
            selected_elements = response.css(selector)
            tags = [el.root.tag for el in selected_elements] if selected_elements else []
            mini_dom[param['param_name']] = {
                "selector": selector,
                "count": len(selected_elements), # how many nodes matched
                "tags": tags                     # type of HTML elements found
            }
        return mini_dom

    def calculate_signature(self, mini_dom):
        serialized = json.dumps(mini_dom, sort_keys=True, ensure_ascii=False)
        return hashlib.sha256(serialized.encode()).hexdigest()

    def compare_and_update(self, industry_module_url_id, new_signature):
        old_signature = get_latest_dom_signature(self.db, industry_module_url_id)
        if old_signature is None or old_signature != new_signature:
            save_dom_signature(self.db, industry_module_url_id, new_signature)
            return old_signature is not None  # True if changed, False if first time
        return False # no change

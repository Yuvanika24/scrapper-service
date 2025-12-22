import urllib.parse
import requests
from dotenv import load_dotenv
import os

load_dotenv()

def get_cse_results(query, num=10, start=1):
    params = {
        "key": os.getenv("API_KEY"),
        "cx": os.getenv("CX_ID"),
        "q": query,
        "num": num,
        "start": start,
        "gl": "us",
        "lr": "lang_en",
    }

    # Build the full request URL
    url = "https://www.googleapis.com/customsearch/v1?" + urllib.parse.urlencode(params)
    
    # Send request to Google CSE
    resp = requests.get(url, timeout=10)
    resp.raise_for_status()

    data = resp.json()

    return [item["link"] for item in data.get("items", [])]

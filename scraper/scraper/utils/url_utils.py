"""
    Normalize URL for dedup comparison.
    - remove query params
    - remove fragments
    - remove trailing slash
"""
from urllib.parse import urlparse, urlunparse

def normalize_url(url: str) -> str:
    parsed = urlparse(url)

    normalized = urlunparse((
        parsed.scheme,
        parsed.netloc.lower(),
        parsed.path.rstrip("/"),
        "",   # params
        "",   # query
        ""    # fragment
    ))

    return normalized

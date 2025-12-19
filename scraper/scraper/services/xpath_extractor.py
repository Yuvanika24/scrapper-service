from lxml import html
from scraper.transformers.transformers import text_clean

def scrape_page_with_xpath(response, keyword):
    tree = html.fromstring(response.text)
    phrase = keyword.lower().strip()
    words = phrase.split()

    result = []
    seen_content = set()

    nodes = tree.xpath("//p | //li | //td | //th | //h1 | //h2 | //h3")

    for node in nodes:
        content = text_clean(" ".join(node.itertext())).strip()
        if not content or content in seen_content:
            continue
        if content.startswith("["):
            continue

        content_lower = content.lower()
        match_count = sum(1 for w in words if w in content_lower)

        if match_count >= max(1, len(words)//2):
            result.append({
                "url": response.url,
                "xpath": node.getroottree().getpath(node),
                "keyword": phrase,
                "content": content[:200] + "..." if len(content) > 200 else content,
                "match_count": match_count
            })
            seen_content.add(content)

    result.sort(key=lambda x: x["match_count"], reverse=True)
    for r in result:
        r.pop("match_count", None)

    return result

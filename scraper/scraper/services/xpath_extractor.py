from lxml import html
from scraper.transformers.transformers import text_clean

def scrape_page_with_xpath(response, keyword):
    tree = html.fromstring(response.text)

    words = keyword.lower().split()
    # words = [keyword.lower()]

    result = []
    seenContent = set()

    nodes = tree.xpath("//p | //li | //td | //th | //h1 | //h2 | //h3")

    for word in words:
        for node in nodes:
            content = text_clean(" ".join(node.itertext()))
            if word in content.lower() and content not in seenContent:
                result.append({
                    "url": response.url,
                    "xpath": node.getroottree().getpath(node),
                    "keyword": word,
                    "content": content[:200] + "..." if len(content) > 200 else content
                })
                seenContent.add(content)

    return result
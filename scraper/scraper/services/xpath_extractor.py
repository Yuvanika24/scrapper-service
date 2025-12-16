from lxml import html
from transformers.transformers import text_clean

def scrape_page_with_xpath(response, keyword):

    tree = html.fromstring(response.text)

    words = keyword.lower().split()
    result = []
    seenContent = set()

    for word in words:

        # Find visible page text that contains the keyword, ignoring scripts and styles
        xpath_query = (
            f'//*[contains(translate(normalize-space(string(.)), '
            f'"ABCDEFGHIJKLMNOPQRSTUVWXYZ", "abcdefghijklmnopqrstuvwxyz"), "{word}") '
            f'and not(self::script or self::style or ancestor::script or ancestor::style)]'
        )

        nodes = tree.xpath(xpath_query)

        for node in nodes:
            content = text_clean("".join(node.itertext()))
            node_xpath = node.getroottree().getpath(node)
            node_xpath = node_xpath[:200] + "..." if len(node_xpath) > 200 else node_xpath
            if content not in seenContent:
                result.append(
                    {
                        "url": response.url,
                        "xpath": node_xpath,
                        "keyword": word,
                        "content": content[:200] + "...", # Truncates to 200 characters
                    }
                )
                seenContent.add(content)
    return result



def extract_content_images(response):

    content_container = response.xpath(
        "//article | //main | //div[contains(@class,'content')]"
    )

    image_urls = content_container.xpath(
        ".//img/@src | .//img/@data-src | .//img/@data-original"
    ).getall()

    image_urls = [
        response.urljoin(img)
        for img in image_urls
        if img
    ]

    image_urls = [
        img for img in image_urls
        if not any(x in img.lower() for x in ["logo", "icon", "sprite", "svg"])
    ]

    return image_urls

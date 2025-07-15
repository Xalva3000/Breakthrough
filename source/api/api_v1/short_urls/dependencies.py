from .schemas import ShortUrl

SHORT_URLS = [
    ShortUrl(
        target_url="http://google.com",
        slug="search",
    ),
    ShortUrl(
        target_url="http://rutube.ru",
        slug="video",
    ),
]




def prefetch_short_url(slug: str):
    url: ShortUrl | None = next((url for url in SHORT_URLS if url.slug == slug), None)

    return url



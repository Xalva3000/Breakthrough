from .schemas import ShortUrl, ShortUrlCreate
from pydantic import BaseModel


class ShortUrlStorage(BaseModel):
    slug_to_short_url: dict[str, ShortUrl] = {}

    def get_all(self) -> list[ShortUrl]:
        return list(self.slug_to_short_url.values())

    def get_by_slug(self, slug: str) -> ShortUrl | None:
        return self.slug_to_short_url.get(slug)

    def create(self, short_url_in: ShortUrlCreate) -> ShortUrl:
        short_url = ShortUrl(
            **short_url_in.model_dump()
        )
        self.slug_to_short_url[short_url.slug] = short_url

        return short_url

    def delete_by_slug(self, slug: str) -> None:
        self.slug_to_short_url.pop(slug, None)

    def delete(self, short_url: ShortUrl):
        self.delete_by_slug(short_url.slug)


storage = ShortUrlStorage()

# SHORT_URLS = [
#     ShortUrl(
#         target_url="http://google.com",
#         slug="search",
#     ),
#     ShortUrl(
#         target_url="http://rutube.ru",
#         slug="video",
#     ),
# ]


u1 = ShortUrlCreate(
    target_url="http://google.com",
    slug="search",
)

u2 = ShortUrlCreate(
    target_url="http://rutube.ru",
    slug="video",
)


storage.create(short_url_in=u1)
storage.create(short_url_in=u2)


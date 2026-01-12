from .schemas import ShortUrl, ShortUrlCreate, ShortUrlUpdate, ShortUrlPartialUpdate
from pydantic import BaseModel, ValidationError
from core import SHORT_URL_STORAGE_PATH as SAVE_FILE
import logging


logger = logging.getLogger(__name__)


class ShortUrlStorage(BaseModel):
    slug_to_short_url: dict[str, ShortUrl] = {}

    def save_state(self):
        SAVE_FILE.write_text(self.model_dump_json(indent=2))
        logger.info("Short url storage state saved.")

    @classmethod
    def from_state(cls):
        logger.info("Short url storage loading...")
        if not SAVE_FILE.exists():
            return ShortUrlStorage()
        return cls.model_validate_json(SAVE_FILE.read_text())

    def init_storage_from_state(self):
        try:
            data = ShortUrlStorage.from_state()
        except ValidationError:
            storage.save_state()
            logger.warning("Storage file rewritten due to validation error.")
            return

        self.slug_to_short_url.update(
            data.slug_to_short_url,
        )

    def get_all(self) -> list[ShortUrl]:
        logger.info("Getting short url list.")
        return list(self.slug_to_short_url.values())

    def get_by_slug(self, slug: str) -> ShortUrl | None:
        logger.info(f"Getting '{slug}' short url.")
        return self.slug_to_short_url.get(slug)

    def create(self, short_url_in: ShortUrlCreate) -> ShortUrl:
        logger.info(f"Creating '{short_url_in.slug}' short url.")
        short_url = ShortUrl(**short_url_in.model_dump())

        self.slug_to_short_url[short_url.slug] = short_url
        # self._save_to_file()
        # self.save_state()

        return short_url

    def update(
        self,
        short_url: ShortUrl,
        short_url_in: ShortUrlUpdate,
    ):
        logger.info(f"Updating '{short_url.slug}' short url.")
        for field_name, value in short_url_in:
            setattr(short_url, field_name, value)

        # self._save_to_file()
        self.save_state()
        return short_url

    def update_partial(
        self,
        short_url: ShortUrl,
        short_url_in: ShortUrlPartialUpdate,
    ):
        new_data = short_url_in.model_dump(exclude_unset=True).items()
        for field_name, value in new_data:
            setattr(short_url, field_name, value)

        # self._save_to_file()
        self.save_state()
        return short_url

    def delete_by_slug(self, slug: str) -> None:
        logger.info(f"Deleting '{slug}' short url.")
        self.slug_to_short_url.pop(slug, None)
        # self._save_to_file()
        self.save_state()

    def delete(self, short_url: ShortUrl):
        self.delete_by_slug(short_url.slug)

    # def __init__(self, **data):
    #     super().__init__(**data)
    #     self.slug_to_short_url = self._load_json_file()

    # def _load_json_file(self) -> dict[str, ShortUrl]:
    #     data = {}
    #     print(os.listdir())
    #     if 'storage_short_url.json' in os.listdir():
    #         try:
    #             with open('storage_short_url.json', 'r', encoding='utf-8') as file:
    #                 loaded_data = json.load(file)
    #                 for slug, obj in loaded_data.items():
    #                     data[slug] = ShortUrl.model_validate_json(obj)
    #                 print(data)
    #         except JSONDecodeError:
    #             return data
    #     return data

    # def _save_to_file(self):
    #     with open('storage_short_url.json', 'w', encoding='utf-8') as file:
    #         print(self.slug_to_short_url.items())
    #         data = {slug: url.model_dump_json() for slug, url in self.slug_to_short_url.items()}
    #         print(data)
    #         json.dump(data, file, ensure_ascii=False, indent=4)


storage = ShortUrlStorage()
# try:
#     storage = ShortUrlStorage.from_state()
# except ValidationError:
#     storage = ShortUrlStorage()

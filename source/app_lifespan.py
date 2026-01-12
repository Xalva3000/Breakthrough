from contextlib import asynccontextmanager
from api.api_v1.short_urls.crud import storage, ShortUrlStorage
from fastapi import FastAPI

from api.api_v1.short_urls.schemas import ShortUrlCreate


def create_default_data(storage: ShortUrlStorage):
    if "search" not in storage.slug_to_short_url:
        u1 = ShortUrlCreate(
            target_url="http://google.com",
            slug="search",
        )
        storage.create(short_url_in=u1)
        print("search url added")
    if "video" not in storage.slug_to_short_url:
        u2 = ShortUrlCreate(
            target_url="http://rutube.ru",
            slug="video",
        )
        storage.create(short_url_in=u2)
        print("video url added")


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Действия до запуска приложения
    storage.init_storage_from_state()
    create_default_data(storage)
    # Функция ставится на паузу на время работы приложения
    yield
    # Действия при завершении работы



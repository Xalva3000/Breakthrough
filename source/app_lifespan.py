from contextlib import asynccontextmanager

from pydantic import AnyHttpUrl

from api.api_v1.books.schemas import PageBase, BookBase
from api.api_v1.short_urls.crud import storage, ShortUrlStorage
from api.api_v1.books.crud import BookStorage
from fastapi import FastAPI

from api.api_v1.short_urls.schemas import ShortUrlCreate


def create_default_urls(storage: ShortUrlStorage):
    if "search" not in storage.slug_to_short_url:
        u1 = ShortUrlCreate(
            target_url=AnyHttpUrl("http://google.com"),
            slug="search",
        )
        storage.create(short_url_in=u1)
        print("search url added")
    if "video" not in storage.slug_to_short_url:
        u2 = ShortUrlCreate(
            target_url=AnyHttpUrl("http://rutube.ru"),
            slug="video",
        )
        storage.create(short_url_in=u2)
        print("video url added")

def create_test_books(book_storage: BookStorage):
    page = PageBase(index=1, text="test_page")
    book = BookBase(title="test", pages={1: page})
    book_storage.create(book)
    print("test book created")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Действия до запуска приложения
    storage.init_storage_from_state()
    create_default_urls(storage)
    book_storage = BookStorage()
    create_test_books(book_storage)
    # Функция ставится на паузу на время работы приложения
    yield
    # Действия при завершении работы

from fastapi import APIRouter
from .short_urls import router as router_short_urls
from .movies import router as router_movies
from.books import router as books_router


router = APIRouter(prefix="/v1")

# Подключение роутера к short_urls
router.include_router(router_short_urls)

# Подключение роутера к movies
router.include_router(router_movies)

# Подключение роутера к books
router.include_router(books_router)

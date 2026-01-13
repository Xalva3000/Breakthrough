from typing import Annotated

from fastapi import APIRouter, Depends
from starlette import status

from api.api_v1.books.dependencies import prefetch_book, prefetch_page, compose_and_create_book
from api.api_v1.books.schemas import BookBase, PageBase

router = APIRouter(prefix="/books")


@router.get(
    path="/{title}/",
    response_model=BookBase,
)
def get_book_by_title(
        book: Annotated[
            BookBase,
            Depends(prefetch_book)
        ],
):
    return book

@router.get(
    path="/{book_title}/{index}/",
    response_model=PageBase,
)
def get_book_page_by_index(
        page: Annotated[
            PageBase,
            Depends(prefetch_page)
        ],
):
    return page


@router.post(
    path="/create",
    response_model=BookBase,
    status_code=status.HTTP_201_CREATED,
)
def create_book(
        book_data: BookBase,
):
    return compose_and_create_book(book_data)
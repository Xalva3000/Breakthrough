from typing import Annotated

from fastapi import APIRouter, Depends
from starlette import status

from api.api_v1.books.dependencies import (
    prefetch_book,
    prefetch_page,
    compose_and_create_book,
    delete_book_by_title,
    insert_page_by_book_title,
)
from api.api_v1.books.schemas import BookBase, PageBase

router = APIRouter(prefix="/books")


@router.get(
    path="/{book_title}/",
    response_model=BookBase,
)
def get_book_by_title(
    book: Annotated[
        BookBase,
        Depends(prefetch_book),
    ],
):
    return book


@router.get(
    path="/{book_title}/{index}",
    response_model=PageBase,
)
def get_book_page_by_index(
    page: Annotated[
        PageBase,
        Depends(prefetch_page),
    ],
):
    return page


@router.post(
    path="/create",
    response_model=BookBase,
    status_code=status.HTTP_201_CREATED,
)
def create_book(book_data: BookBase):
    return compose_and_create_book(book_data)


@router.delete(
    path="/{book_title}/delete",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_book(book_title: str):
    return delete_book_by_title(book_title)


@router.patch(
    path="/{book_title}/{index}",
    response_model=BookBase,
    status_code=status.HTTP_200_OK,
)
def insert_or_replace_page(book_title: str, index: str, new_page: PageBase):
    return insert_page_by_book_title(book_title, new_page)

from fastapi import HTTPException
from starlette import status

from api.api_v1.books.crud import book_storage as storage
from api.api_v1.books.schemas import BookBase, PageBase


def prefetch_book(book_title: str):
    book: BookBase = storage.get_book(book_title)
    if book:
        return book
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"BOOK {book_title} not found",
    )


def prefetch_page(book_title: str, index: str):
    print(f"{book_title=}, {index=}")
    page: PageBase = storage.get_page(book_title=book_title, index=index)
    print(page)
    if page:
        return page
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"PAGE {index} not found",
    )


def compose_and_create_book(book_data):
    try:
        return storage.create(book_data)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Book format is incorrect",
        )


def delete_book_by_title(title):
    try:
        return storage.delete_book(title)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Book format is incorrect",
        )


def insert_page_by_book_title(book_title, new_page):
    return storage.insert_page(book_title, new_page)

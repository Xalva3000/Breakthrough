from fastapi import HTTPException
from starlette import status

from api.api_v1.books.crud import book_storage

def prefetch_book(title):
    book = book_storage.get_book(title)
    if book:
        return book
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"BOOK {title} not found",
    )
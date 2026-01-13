from typing import Annotated

from fastapi import APIRouter, Depends

from api.api_v1.books.dependencies import prefetch_book
from api.api_v1.books.schemas import BookBase


router = APIRouter(prefix="/books")


@router.get(
    path="/{title}/",
    response_model=BookBase,
)
def get_book_by_title(title: str, book: Annotated[BookBase, Depends(prefetch_book)]):
    return book
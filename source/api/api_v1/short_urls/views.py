from typing import Annotated

# from pydantic import AnyHttpUrl
# from annotated_types import Len

from .schemas import ShortUrl, ShortUrlCreate
from fastapi.responses import RedirectResponse
from .dependencies import prefetch_short_url, storage
from fastapi import Request, HTTPException, status, Depends, APIRouter, Form


router = APIRouter(prefix="/short-urls")


@router.get("/list/", response_model=list[ShortUrl])
def read_short_urls_list() -> list[ShortUrl]:
    return storage.get_all()


@router.get("/{slug}")
@router.get("/{slug}/")
def redirect_short_url(slug, url: Annotated[ShortUrl, Depends(prefetch_short_url)]):
    if url:
        return RedirectResponse(url=url.target_url)
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=f"URL {slug!r} not found"
    )


@router.post(
    "/",
    response_model=ShortUrl,
    status_code=status.HTTP_201_CREATED,
)
def create_short_url(
    short_url_create: ShortUrlCreate,
):
    new_url = ShortUrl(
        **short_url_create.model_dump(),
    )

    storage.create(new_url)

    return new_url


@router.delete(
    "/{slug}/",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "SHORT_URL not found",
            "content": {
                "application/json": {"example": {"detail": "URL 'slug' not found"}}
            },
        }
    },
)
def delete_short_url(url: Annotated[ShortUrl, Depends(prefetch_short_url)]) -> None:
    # storage.delete_by_slug(slug)
    storage.delete(short_url=url)

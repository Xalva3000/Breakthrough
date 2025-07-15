from typing import Annotated

from pydantic import AnyHttpUrl

from annotated_types import Len

from .schemas import ShortUrl, ShortUrlCreate
from fastapi.responses import RedirectResponse
from .dependencies import prefetch_short_url, SHORT_URLS
from fastapi import Request, HTTPException, status, Depends, APIRouter, Form


router = APIRouter(prefix="/short-urls")


@router.get("/list/")
def read_short_urls_list():
    return SHORT_URLS


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
    print(short_url_create)
    print(type(short_url_create))
    return ShortUrl(
        **short_url_create.model_dump(),
    )

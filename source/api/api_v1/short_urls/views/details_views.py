from typing import Annotated

# from pydantic import AnyHttpUrl
# from annotated_types import Len

from api.api_v1.short_urls.schemas import (
    ShortUrl,
    ShortUrlCreate,
    ShortUrlUpdate,
    ShortUrlPartialUpdate,
    ShortUrlRead,
)
from fastapi.responses import RedirectResponse
from api.api_v1.short_urls.dependencies import (
    prefetch_short_url,
    storage,
    save_storage_state,
)
from fastapi import Request, HTTPException, status, Depends, APIRouter, Form

custom_responses = {
    status.HTTP_404_NOT_FOUND: {
        "description": "SHORT_URL not found",
        "content": {
            "application/json": {
                "example": {"detail": "URL 'slug' not found"},
            },
        },
    },
}

router = APIRouter(prefix="/{slug}", responses=custom_responses)

ShortUrlBySlug = Annotated[ShortUrl, Depends(prefetch_short_url)]


@router.get("/")
def redirect_short_url(
    slug,
    url: ShortUrlBySlug,
):
    if url:
        return RedirectResponse(url=url.target_url)
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=f"URL {slug!r} not found"
    )


@router.delete(
    "/",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_short_url(
    url: ShortUrlBySlug,
) -> None:
    # storage.delete_by_slug(slug)
    storage.delete(short_url=url)


@router.put(
    "/",
    response_model=ShortUrl,
)
def update_short_url(
    url: ShortUrlBySlug,
    new_url: ShortUrlUpdate,
):
    return storage.update(url, new_url)


@router.patch(
    "/",
    response_model=ShortUrlRead,
)
def update_short_url_partial(
    url: ShortUrlBySlug,
    new_url: ShortUrlPartialUpdate,
):
    return storage.update_partial(url, new_url)

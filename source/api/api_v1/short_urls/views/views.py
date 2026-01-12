from typing import Annotated

# from pydantic import AnyHttpUrl
# from annotated_types import Len

from api.api_v1.short_urls.schemas import ShortUrl, ShortUrlCreate, ShortUrlRead
# from fastapi.responses import RedirectResponse
from api.api_v1.short_urls.dependencies import (
    prefetch_short_url,
    storage,
    save_storage_state,
    api_token_required,
    user_basic_auth_required,
)
from fastapi import Request, HTTPException, status, Depends, APIRouter, Form, BackgroundTasks


router = APIRouter(
    prefix="/short-urls",
    dependencies=[
        Depends(save_storage_state),
        # Depends(api_token_required),
    ]
)


@router.get(
    "/list/",
    response_model=list[ShortUrlRead]
)
def read_short_urls_list() -> list[ShortUrl]:
    return storage.get_all()



@router.post(
    "/",
    response_model=ShortUrl,
    status_code=status.HTTP_201_CREATED,
    dependencies=[
        Depends(user_basic_auth_required),
    ]
)
def create_short_url(
    short_url_create: ShortUrlCreate,
):
    new_url = ShortUrl(
        **short_url_create.model_dump(),
    )

    storage.create(new_url)

    return new_url




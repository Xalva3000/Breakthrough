import logging

from fastapi import (
        HTTPException, 
        BackgroundTasks, 
        Request,
        # Query,
        Header,
        status,
        Depends,
)
from fastapi.security import (
    HTTPBearer,
    HTTPAuthorizationCredentials,
    HTTPBasic,
    HTTPBasicCredentials,
)
from .schemas import ShortUrl
from .crud import storage
from core import API_TOKENS, USERS_DB
from typing import Annotated


logger = logging.getLogger(__name__)


static_api_token = HTTPBearer(
    scheme_name="Static API Token",
    description="",
    auto_error=False,
)

user_basic_auth = HTTPBasic(
    scheme_name="Basic Auth",
    description="Basic UserName + password auth",
    auto_error=False,
)

UNSAFE_METHODS = {
        "PUT",
        "PATCH",
        "POST",
        "UPDATE",
        "DELETE",
    }

def prefetch_short_url(
        slug: str
) -> ShortUrl:

    url: ShortUrl | None = storage.get_by_slug(slug=slug)
    # next((url for url in SHORT_URLS if url.slug == slug), None))

    if url:
        return url

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"URL {slug!r} not found",
    )

def save_storage_state(
        request: Request,
        background_tasks: BackgroundTasks,
):
    yield
    if request.method in UNSAFE_METHODS:
        background_tasks.add_task(storage.save_state)
        logger.info("Storage save state task is added to pool")


def api_token_required(
        request: Request,
        api_token: Annotated[
            HTTPAuthorizationCredentials | None,
            Depends(static_api_token),
        ] = None,
    ) -> None:
    #  Header(alias="x-auth-token"),
    if not api_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token is required",
        )

    logger.info("API Token received")

    if request.method in UNSAFE_METHODS:
        if api_token not in API_TOKENS:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="invalid token",
            )

def user_basic_auth_required(
        credentials: Annotated[
                HTTPBasicCredentials | None,
                Depends(user_basic_auth),
            ] = None,
):
    if (
        credentials
        and credentials.username in USERS_DB
        and USERS_DB[credentials.username] == credentials.password
    ):
        return

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail= "UserCredentials required. Invalid credentials.",
        headers={"WWW-Authenticate": "Basic"},
    )

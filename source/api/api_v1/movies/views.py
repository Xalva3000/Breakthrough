from typing import Annotated
from .schemas import Movie
from fastapi.responses import RedirectResponse
from .dependencies import prefetch_movie_data, MOVIES_LIST
from fastapi import Request, HTTPException, status, Depends, APIRouter


router = APIRouter(prefix="/movies")


@router.get("/list/")
def get_movies_list():
    return MOVIES_LIST


@router.get("/{movie_id}/")
def get_movie_data_by_id(
    movie_id, movie_data: Annotated[Movie, Depends(prefetch_movie_data)]
):
    if movie_data:
        return {"movie_data": movie_data}
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Movie not found. Searched id: {movie_id!r}",
    )

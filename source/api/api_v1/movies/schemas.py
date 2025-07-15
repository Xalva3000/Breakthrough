from pydantic import BaseModel


class MovieBase(BaseModel):
    movie_id: int
    name: str
    description: str


class Movie(MovieBase):
    """
    Movie model
    """

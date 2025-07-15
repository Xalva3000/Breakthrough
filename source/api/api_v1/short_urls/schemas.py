from pydantic import BaseModel, AnyHttpUrl
from typing import Annotated
from annotated_types import Len


class ShortUrlBase(BaseModel):
    """
    Базовая модель короткой ссылки
    """
    target_url: AnyHttpUrl
    slug: str


class ShortUrl(ShortUrlBase):
    """
    Основная модель ShortUrl
    """

class ShortUrlCreate(ShortUrlBase):
    """
    Модель для создания короткой ссылки
    """
    slug: Annotated[str, Len(min_length=3, max_length=10),]

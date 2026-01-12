from pydantic import BaseModel, AnyHttpUrl
from typing import Annotated
from annotated_types import Len, MinLen, MaxLen


DescriptionString = Annotated[
        str,
        MinLen(0),
        MaxLen(200),
    ]

class ShortUrlBase(BaseModel):
    """
    Базовая модель короткой ссылки
    """
    target_url: AnyHttpUrl
    slug: str
    description: DescriptionString  = ""


class ShortUrl(ShortUrlBase):
    """
    Основная модель ShortUrl
    """
    visits: int = 42

class ShortUrlCreate(ShortUrlBase):
    """
    Модель для создания короткой ссылки
    """
    slug: Annotated[str, Len(min_length=3, max_length=10),]

class ShortUrlUpdate(ShortUrlBase):
    """
    Модель для обновления
    """

class ShortUrlPartialUpdate(ShortUrlBase):
    """
    Модель для частичного обновления
    """
    target_url: AnyHttpUrl | None = None
    description: DescriptionString | None = None

class ShortUrlRead(ShortUrlBase):
    """
    Модель для вывода
    """
    slug: str


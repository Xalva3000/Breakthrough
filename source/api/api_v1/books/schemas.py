from pydantic import BaseModel, Field, field_validator


class PageBase(BaseModel):
    index: int = 1
    text: str = Field(min_length=1, max_length=5000)


class BookBase(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    pages: dict[str, PageBase] = {}

    @field_validator("pages")
    @classmethod
    def validate_page_numbers(cls, pages):
        if pages:
            expected = list(range(1, len(pages) + 1))
            actual = sorted(map(int, pages.keys()))
            if actual != expected:
                raise ValueError(
                    "Номера страниц должны начинаться с 1 и идти последовательно"
                )
        return pages

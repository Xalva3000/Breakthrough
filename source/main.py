import uvicorn


from fastapi import (
    FastAPI,
    Request,
    Depends,
    status,
    HTTPException,
)
from fastapi.responses import RedirectResponse
from api import router as api_router
from api.api_v1.short_urls.schemas import ShortUrl
from api.api_v1.short_urls.dependencies import prefetch_short_url
from typing import Annotated


# Инициализация fastapi класса
app = FastAPI(
    title="Breakthrough",
)

# Подключение всех роутеров
app.include_router(api_router)


@app.get(
    "/",
)
def greet(
    request: Request,
    name: str = "Alex"
):
    docs_url = request.url.replace(path="/docs")

    return {
        "message": f"Hello, {name}",
        "docs": str(docs_url),
    }



@app.get("/r/{slug}")
@app.get("/r/{slug}/")
def redirect_short_url(slug, url: Annotated[ShortUrl, Depends(prefetch_short_url)]):
    if url:
        return RedirectResponse(url=url.target_url)
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=f"URL {slug!r} not found"
    )


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)


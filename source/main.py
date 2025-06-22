import uvicorn
from fastapi import FastAPI, Request


app = FastAPI(
    title="Breakthrough",
)


@app.get("/")
def greet(
    request: Request,
    name: str = "Alex",
):
    docs_url = request.url.replace(
        path="/docs",
        query="",
    )
    return {
        "message": f"Hello, {name}!",
        "docs_url": docs_url,
    }


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)

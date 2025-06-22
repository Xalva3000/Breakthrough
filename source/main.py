import uvicorn
from fastapi import FastAPI


app = FastAPI(
    title="Breakthrough",
)


@app.get("/")
def greet():
    return {"message": f"Hello"}


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)

from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def greet(name):
    print(f"Hello, {name}")


if __name__ == '__main__':
    greet("Alex")
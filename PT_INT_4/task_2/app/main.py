from fastapi import FastAPI
import uvicorn

app = FastAPI()

@app.get("/healthz")
def func():
    return "200 OK"


if __name__ == "__main__":
        uvicorn.run("main:app", host="0.0.0.0", port=80)

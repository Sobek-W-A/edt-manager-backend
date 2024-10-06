from fastapi import FastAPI
from starlette.responses import RedirectResponse

app = FastAPI()

@app.get("/")
async def root():
    return RedirectResponse(url="/docs")

@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}



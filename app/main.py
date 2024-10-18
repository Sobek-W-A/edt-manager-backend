from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse

from app.models.Tags import Tag
from app.routes import auth, user

from app.utils.databases.db import startup_databases

# Array for the routes descriptions and names.
tags_metadata: list[dict[str, str]] = [
    {
        "name": "user",
        "description": "User operations."
    },
    {
        "name": "auth",
        "description": "Authentication endpoints."
    }
]

# Creation of the main router
app: FastAPI = FastAPI(title="SOBEK W.A. API",
              description="API For the SOBEK W.A web application",
              openapi_tags=tags_metadata)

# List of requests origins that are allowed for the API
# IMPORTANT NOTICE: Using the wildcard * is dangerous:
# It will allow all request sources.
# Furthermore, with authentication enabled, it will not work.
# Listing authorized sources is MANDATORY.
origins: list[str] = [
    "http://localhost:5173",
    "https://localhost:5173",
]

# TODO : Check this issue.
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Importing API routes :
app.include_router(user.userRouter, prefix="/user", tags=["user"])
app.include_router(auth.authRouter, prefix="/auth", tags=["auth"])

# TODO : Fix the deprecated event.
@app.on_event("startup")
async def startup() -> None:
    await startup_databases(app=app)


# Root path: Redirecting to the documentation.
@app.get("/")
async def root() -> RedirectResponse:
    return RedirectResponse(url="/docs")
"""
Starting point of the API.
This is where the FastAPI app is defined, as well as the different tags for the documentation.
Also contains the startup operations (like DB init).
"""
from contextlib import asynccontextmanager
from typing import Any, AsyncGenerator

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.responses import RedirectResponse

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

@asynccontextmanager
async def lifespan(application: FastAPI) -> AsyncGenerator[Any, Any]:
    """
    This method indicates what the method needs to do at startup.
    """
    # Démarrage des bases de données
    await startup_databases(app=application)
    yield
    # Code pour fermer les bases de données (si nécessaire)


# Creation of the main router
app: FastAPI = FastAPI(title="SOBEK W.A. API",
                       description="API For the SOBEK W.A web application",
                       openapi_tags=tags_metadata,
                       lifespan=lifespan)

@app.exception_handler(AssertionError)
async def assertion_exception_handler(request: Request, exc: AssertionError) -> JSONResponse:
    return JSONResponse(
        status_code=400,
        content={"detail": str(exc)}
    )

# List of requests origins that are allowed for the API
# IMPORTANT NOTICE: Using the wildcard * is dangerous:
# It will allow all request sources.
# Furthermore, with authentication enabled, it will not work.
# Listing authorized sources is MANDATORY.
origins: list[str] = [
    "http://localhost:5173",
    "https://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Importing API routes :
app.include_router(user.userRouter, tags=["user"])
app.include_router(auth.authRouter, tags=["auth"])

# Root path: Redirecting to the documentation.
@app.get("/")
async def root() -> RedirectResponse:
    """
    Root method.
    Redirects to the documentation.
    """
    return RedirectResponse(url="/docs")

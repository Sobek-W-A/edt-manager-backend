"""
Starting point of the API.
This is where the FastAPI app is defined, as well as the different tags for the documentation.
Also contains the startup operations (like DB init).
"""
from contextlib import asynccontextmanager
from typing import Any, AsyncGenerator, cast

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse

from app.models.aliases import AuthenticatedAccount
from app.routes import account, auth, profile, role, ue, course, status, affectation, node, academic_year
from app.routes.tags import Tag

from app.services import ExportService
from app.utils.databases.db import startup_databases
from app.utils.printers import print_info

# Array for the routes descriptions and names.
tags_metadata: list[Tag] = [
    account.tag,
    auth.tag,
    profile.tag,
    role.tag,
    node.tag,
    ue.tag,
    course.tag,
    status.tag,
    affectation.tag,
    academic_year.tag
]

@asynccontextmanager
async def lifespan(application: FastAPI) -> AsyncGenerator[Any, Any]:
    """
    This method indicates what the method needs to do at startup.
    """
    # Démarrage des bases de données
    print_info("Starting databases...")
    await startup_databases(app=application)
    yield
    # Code pour fermer les bases de données (si nécessaire)


# Creation of the main router
app: FastAPI = FastAPI(title="SOBEK W.A. API",
                       description="API For the SOBEK W.A web application",
                       openapi_tags=cast(list[dict[str, str]], tags_metadata),
                       lifespan=lifespan)

# List of requests origins that are allowed for the API
# IMPORTANT NOTICE: Using the wildcard * is dangerous:
# It will allow all request sources.
# Furthermore, with authentication enabled, it will not work.
# Listing authorized sources is MANDATORY.
origins: list[str] = [
    "http://localhost:5173",
    "https://localhost:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Importing API routes :
app.include_router(account.accountRouter,             tags=[account.tag["name"]])
app.include_router(auth.authRouter,                   tags=[auth.tag["name"]])
app.include_router(profile.profileRouter,             tags=[profile.tag["name"]])
app.include_router(role.roleRouter,                   tags=[role.tag["name"]])
app.include_router(node.nodeRouter,                   tags=[node.tag["name"]])
app.include_router(ue.ueRouter,                       tags=[ue.tag["name"]])
app.include_router(course.courseRouter,               tags=[course.tag["name"]])
app.include_router(status.statusRouter,               tags=[status.tag["name"]])
app.include_router(affectation.affectationRouter,     tags=[affectation.tag["name"]])
app.include_router(academic_year.academic_yearRouter, tags=[academic_year.tag["name"]])

# Root path: Redirecting to the documentation.
@app.get("/")
async def root() -> RedirectResponse:
    """
    Root method.
    Redirects to the documentation.
    """
    return RedirectResponse(url="/docs")

@app.get("/export")
async def export_data(academic_year: int, current_accont: AuthenticatedAccount):
    """
    Exports the database's content.
    """
    await ExportService.export_data(academic_year, current_accont)

@app.post("/import")
async def import_data(academic_year: int, current_accont: AuthenticatedAccount):
    """
    Imports data into the database.
    """
    await ExportService.import_data(academic_year, current_accont)

from fastapi import FastAPI
from app.database import Base, engine

from .router.auth import router as auth_router
from .router.users import router as users_router
from .router.posts import router as posts_router

app = FastAPI(
    debug=True,
    title="CRUD APIs build on FastAPI",
    description="This is a sample FastAPI application.",
    version="1.0.0",
    docs_url="/api/docs",  # Specify the URL for API documentation
    redoc_url="/api/redoc",  # Specify the URL for ReDoc documentation
    openapi_url="/api/openapi.json",  # Specify the URL for the OpenAPI JSON document
)

Base.metadata.create_all(engine)

app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(users_router, prefix="/users", tags=["users"])
app.include_router(posts_router, prefix="/posts", tags=["posts"])

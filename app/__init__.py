from fastapi import FastAPI

app = FastAPI(
    debug=True,
    title="CRUD APIs build on FastAPI",
    description="This is a sample FastAPI application.",
    version="1.0.0",
    docs_url="/api/docs",  # Specify the URL for API documentation
    redoc_url="/api/redoc",  # Specify the URL for ReDoc documentation
    openapi_url="/api/openapi.json",  # Specify the URL for the OpenAPI JSON document
)

from . import main

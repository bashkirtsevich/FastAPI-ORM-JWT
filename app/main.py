from fastapi import FastAPI

from .api import api_router
from .settings import settings

app = FastAPI(
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

app.include_router(api_router, prefix=settings.API_V1_STR)

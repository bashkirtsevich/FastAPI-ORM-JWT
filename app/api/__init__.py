from fastapi import APIRouter

from .user.views import router as user_router

api_router = APIRouter()
api_router.include_router(user_router, tags=["user"])

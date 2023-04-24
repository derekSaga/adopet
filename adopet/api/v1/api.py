from api.v1.routes.user import user_view
from fastapi import APIRouter

api_router = APIRouter()

api_router.include_router(user_view.router, prefix="/user", tags=["user"])

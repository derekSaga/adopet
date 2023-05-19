from api.views.v1.routes.user import tutor_view
from api.views.v1.routes.user import user_view
from fastapi import APIRouter

api_router = APIRouter()

api_router.include_router(user_view.router, prefix="/user", tags=["user"])
api_router.include_router(tutor_view.router, prefix="/tutor", tags=["tutor"])

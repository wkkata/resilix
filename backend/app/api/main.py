from fastapi import APIRouter

from app.api.routes import items, login, private, users, utils, experiences, education
from app.api.endpoints import project

api_router = APIRouter()
api_router.include_router(login.router)
api_router.include_router(users.router)
api_router.include_router(items.router)
api_router.include_router(private.router)
api_router.include_router(utils.router)
api_router.include_router(experiences.router, prefix="/experiences", tags=["experiences"])
api_router.include_router(education.router, prefix="/education", tags=["education"])
api_router.include_router(project.router, prefix="/projects", tags=["projects"])

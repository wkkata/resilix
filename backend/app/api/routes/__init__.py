from fastapi import APIRouter

from app.api.routes import education, experiences, geo, items, login, private, users, utils

api_router = APIRouter()

api_router.include_router(login.router, tags=["login"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(utils.router, prefix="/utils", tags=["utils"])
api_router.include_router(items.router, prefix="/items", tags=["items"])
api_router.include_router(private.router, prefix="/private", tags=["private"])
api_router.include_router(geo.router, prefix="/geo", tags=["geo"])
api_router.include_router(experiences.router, prefix="/experiences", tags=["experiences"])
api_router.include_router(education.router, prefix="/education", tags=["education"])
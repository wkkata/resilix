from fastapi import APIRouter

from app.api.routes import items, login, private, users, utils, experiences, education, coursework, involvement
from app.api.endpoints import project, skill, certificate

api_router = APIRouter()
api_router.include_router(login.router)
api_router.include_router(users.router)
api_router.include_router(items.router)
api_router.include_router(private.router)
api_router.include_router(utils.router)
api_router.include_router(experiences.router, prefix="/experiences", tags=["experiences"])
api_router.include_router(education.router, prefix="/education", tags=["education"])
api_router.include_router(project.router, prefix="/projects", tags=["projects"])
api_router.include_router(skill.router, prefix="/skills", tags=["skills"])
api_router.include_router(
    certificate.router, prefix="/api/v1/certificates", tags=["certificates"]
)
api_router.include_router(coursework.router, prefix="/courseworks", tags=["courseworks"])
api_router.include_router(involvement.router, prefix="/involvements", tags=["involvements"])

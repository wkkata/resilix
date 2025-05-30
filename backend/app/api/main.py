from fastapi import APIRouter

<<<<<<< Updated upstream
from app.api.routes import items, login, private, users, utils, experiences, education, coursework, involvement, project, skill, certificate
=======
from app.api.routes import items, login, openai, private, users, utils
from app.core.config import settings
>>>>>>> Stashed changes

api_router = APIRouter()
api_router.include_router(login.router)
api_router.include_router(users.router)
api_router.include_router(items.router)
<<<<<<< Updated upstream
api_router.include_router(private.router)
api_router.include_router(utils.router)
api_router.include_router(experiences.router, prefix="/experiences", tags=["experiences"])
api_router.include_router(education.router, prefix="/education", tags=["education"])
api_router.include_router(project.router, prefix="/projects", tags=["projects"])
api_router.include_router(skill.router, prefix="/skills", tags=["skills"])
api_router.include_router(certificate.router, prefix="/certificates", tags=["certificates"])
api_router.include_router(coursework.router, prefix="/courseworks", tags=["courseworks"])
api_router.include_router(involvement.router, prefix="/involvements", tags=["involvements"])
=======
api_router.include_router(openai.router)


if settings.ENVIRONMENT == "local":
    api_router.include_router(private.router)
>>>>>>> Stashed changes

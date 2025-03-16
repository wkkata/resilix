from typing import Any
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from app import crud
from app.api import deps
from app.models import Project, ProjectCreate, ProjectUpdate, ProjectPublic, User

router = APIRouter()

@router.post("/", response_model=ProjectPublic)
def create_project(
    *,
    session: Session = Depends(deps.get_session),
    project_in: ProjectCreate,
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    """Create new project for current user."""
    project = crud.create_project(session=session, project_in=project_in, user_id=current_user.id)
    return project

@router.get("/", response_model=list[ProjectPublic])
def read_projects(
    *,
    session: Session = Depends(deps.get_session),
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    """Get all projects for current user."""
    projects = crud.get_projects(session=session, user_id=current_user.id)
    return projects

@router.put("/{project_id}", response_model=ProjectPublic)
def update_project(
    *,
    session: Session = Depends(deps.get_session),
    project_id: UUID,
    project_in: ProjectUpdate,
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    """Update project."""
    project = crud.get_projects(session=session, user_id=current_user.id)
    if not project:
        raise HTTPException(
            status_code=404,
            detail="Project not found",
        )
    project = crud.update_project(
        session=session, db_project=project, project_in=project_in
    )
    return project

@router.delete("/{project_id}")
def delete_project(
    *,
    session: Session = Depends(deps.get_session),
    project_id: UUID,
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    """Delete project."""
    project = crud.get_projects(session=session, user_id=current_user.id)
    if not project:
        raise HTTPException(
            status_code=404,
            detail="Project not found",
        )
    crud.delete_project(session=session, project_id=project_id)
    return {"message": "Project deleted successfully"}
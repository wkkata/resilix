from datetime import date
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from app import crud
from app.api import deps
from app.models import Experience, ExperienceCreate, ExperiencePublic, ExperienceUpdate, User

router = APIRouter()


@router.post("/", response_model=ExperiencePublic)
def create_experience(
    *,
    session: Annotated[Session, Depends(deps.get_session)],
    current_user: Annotated[User, Depends(deps.get_current_user)],
    experience_in: ExperienceCreate,
) -> Experience:
    try:
        return crud.create_experience(
            session=session, experience_in=experience_in, user_id=current_user.id
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.get("/", response_model=list[ExperiencePublic])
def get_experiences(
    *,
    session: Annotated[Session, Depends(deps.get_session)],
    current_user: Annotated[User, Depends(deps.get_current_user)],
) -> list[Experience]:
    return crud.get_experiences(session=session, user_id=current_user.id)


@router.put("/{experience_id}", response_model=ExperiencePublic)
def update_experience(
    *,
    session: Annotated[Session, Depends(deps.get_session)],
    current_user: Annotated[User, Depends(deps.get_current_user)],
    experience_id: UUID,
    experience_in: ExperienceUpdate,
) -> Experience:
    statement = crud.select(Experience).where(
        Experience.id == experience_id, Experience.user_id == current_user.id
    )
    db_experience = session.exec(statement).first()
    if not db_experience:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Experience not found",
        )
    try:
        return crud.update_experience(
            session=session, db_experience=db_experience, experience_in=experience_in
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.delete("/{experience_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_experience(
    *,
    session: Annotated[Session, Depends(deps.get_session)],
    current_user: Annotated[User, Depends(deps.get_current_user)],
    experience_id: UUID,
) -> None:
    statement = crud.select(Experience).where(
        Experience.id == experience_id, Experience.user_id == current_user.id
    )
    db_experience = session.exec(statement).first()
    if not db_experience:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Experience not found",
        )
    crud.delete_experience(session=session, experience_id=experience_id)
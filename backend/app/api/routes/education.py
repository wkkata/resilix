import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from app import crud
from app.api import deps
from app.models import Education, EducationCreate, EducationUpdate, User

router = APIRouter()


@router.post("/", response_model=Education)
def create_education(
    *,
    session: Annotated[Session, Depends(deps.get_session)],
    education_in: EducationCreate,
    current_user: Annotated[User, Depends(deps.get_current_user)],
) -> Education:
    """Create new education."""
    education = crud.create_education(
        session=session, education_in=education_in, user_id=current_user.id
    )
    return education


@router.get("/", response_model=list[Education])
def read_educations(
    *,
    session: Annotated[Session, Depends(deps.get_session)],
    current_user: Annotated[User, Depends(deps.get_current_user)],
) -> list[Education]:
    """Retrieve educations."""
    educations = crud.get_educations(session=session, user_id=current_user.id)
    return educations


@router.put("/{education_id}", response_model=Education)
def update_education(
    *,
    session: Annotated[Session, Depends(deps.get_session)],
    education_id: uuid.UUID,
    education_in: EducationUpdate,
    current_user: Annotated[User, Depends(deps.get_current_user)],
) -> Education:
    """Update an education."""
    statement = crud.select(Education).where(
        Education.id == education_id, Education.user_id == current_user.id
    )
    education = session.exec(statement).first()
    if not education:
        raise HTTPException(status_code=404, detail="Education not found")
    education = crud.update_education(
        session=session, db_education=education, education_in=education_in
    )
    return education


@router.delete("/{education_id}")
def delete_education(
    *,
    session: Annotated[Session, Depends(deps.get_session)],
    education_id: uuid.UUID,
    current_user: Annotated[User, Depends(deps.get_current_user)],
) -> None:
    """Delete an education."""
    statement = crud.select(Education).where(
        Education.id == education_id, Education.user_id == current_user.id
    )
    education = session.exec(statement).first()
    if not education:
        raise HTTPException(status_code=404, detail="Education not found")
    crud.delete_education(session=session, education_id=education_id)
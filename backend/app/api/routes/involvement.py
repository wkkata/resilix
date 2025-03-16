from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from app import crud
from app.api import deps
from app.models import Involvement, InvolvementCreate, InvolvementPublic, InvolvementUpdate, User

router = APIRouter()


@router.post("/", response_model=InvolvementPublic)
def create_involvement(
    *,
    session: Annotated[Session, Depends(deps.get_session)],
    current_user: Annotated[User, Depends(deps.get_current_user)],
    involvement_in: InvolvementCreate,
) -> Involvement:
    return crud.create_involvement(
        session=session, involvement_in=involvement_in, user_id=current_user.id
    )


@router.get("/", response_model=list[InvolvementPublic])
def get_involvements(
    *,
    session: Annotated[Session, Depends(deps.get_session)],
    current_user: Annotated[User, Depends(deps.get_current_user)],
) -> list[Involvement]:
    return crud.get_involvements(session=session, user_id=current_user.id)


@router.put("/{involvement_id}", response_model=InvolvementPublic)
def update_involvement(
    *,
    session: Annotated[Session, Depends(deps.get_session)],
    current_user: Annotated[User, Depends(deps.get_current_user)],
    involvement_id: UUID,
    involvement_in: InvolvementUpdate,
) -> Involvement:
    statement = select(Involvement).where(
        Involvement.id == involvement_id, Involvement.user_id == current_user.id
    )
    db_involvement = session.exec(statement).first()
    if not db_involvement:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Involvement not found",
        )
    return crud.update_involvement(
        session=session, db_involvement=db_involvement, involvement_in=involvement_in
    )


@router.delete("/{involvement_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_involvement(
    *,
    session: Annotated[Session, Depends(deps.get_session)],
    current_user: Annotated[User, Depends(deps.get_current_user)],
    involvement_id: UUID,
) -> None:
    statement = select(Involvement).where(
        Involvement.id == involvement_id, Involvement.user_id == current_user.id
    )
    db_involvement = session.exec(statement).first()
    if not db_involvement:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Involvement not found",
        )
    crud.delete_involvement(session=session, involvement_id=involvement_id)
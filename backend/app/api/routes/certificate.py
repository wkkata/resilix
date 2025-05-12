from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from app import crud
from app.api import deps
from app.models import Certificate, CertificateCreate, CertificateUpdate, User

router = APIRouter()


@router.post("/", response_model=Certificate)
def create_certificate(
    *,
    session: Session = Depends(deps.get_session),
    certificate_in: CertificateCreate,
    current_user: User = Depends(deps.get_current_user),
) -> Certificate:
    certificate = crud.create_certificate(
        session=session, certificate_in=certificate_in, user_id=current_user.id
    )
    return certificate


@router.get("/", response_model=list[Certificate])
def read_certificates(
    *,
    session: Session = Depends(deps.get_session),
    current_user: User = Depends(deps.get_current_user),
) -> list[Certificate]:
    certificates = crud.get_certificates(session=session, user_id=current_user.id)
    return certificates


@router.put("/{certificate_id}", response_model=Certificate)
def update_certificate(
    *,
    session: Session = Depends(deps.get_session),
    certificate_id: UUID,
    certificate_in: CertificateUpdate,
    current_user: User = Depends(deps.get_current_user),
) -> Certificate:
    statement = select(Certificate).where(
        Certificate.id == certificate_id, Certificate.user_id == current_user.id
    )
    certificate = session.exec(statement).first()
    if not certificate:
        raise HTTPException(status_code=404, detail="Certificate not found")
    certificate = crud.update_certificate(
        session=session, db_certificate=certificate, certificate_in=certificate_in
    )
    return certificate


@router.delete("/{certificate_id}")
def delete_certificate(
    *,
    session: Session = Depends(deps.get_session),
    certificate_id: UUID,
    current_user: User = Depends(deps.get_current_user),
) -> None:
    statement = select(Certificate).where(
        Certificate.id == certificate_id, Certificate.user_id == current_user.id
    )
    certificate = session.exec(statement).first()
    if not certificate:
        raise HTTPException(status_code=404, detail="Certificate not found")
    crud.delete_certificate(session=session, certificate_id=certificate_id)
    return {"message": "Certificate deleted successfully"}
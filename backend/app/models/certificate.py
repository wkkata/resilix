from datetime import datetime
from typing import Optional, TYPE_CHECKING
import uuid

from sqlmodel import Field, SQLModel, Relationship

if TYPE_CHECKING:
    from app.models.user import User

class CertificateBase(SQLModel):
    certificate_name: str = Field(index=True)
    institution: str = Field(index=True)
    issue_date: datetime
    description: Optional[str] = None

class Certificate(CertificateBase, table=True):
    id: Optional[uuid.UUID] = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="user.id")
    user: "User" = Relationship(back_populates="certificates")

class CertificateCreate(CertificateBase):
    pass

class CertificateUpdate(SQLModel):
    certificate_name: Optional[str] = None
    institution: Optional[str] = None
    issue_date: Optional[datetime] = None
    description: Optional[str] = None

class CertificatePublic(CertificateBase):
    id: uuid.UUID
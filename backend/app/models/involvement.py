import uuid
from datetime import date
from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel, Session, select

if TYPE_CHECKING:
    from .user import User


class InvolvementBase(SQLModel):
    role: str = Field(max_length=255)
    organization: str = Field(max_length=255)
    start_date: date
    end_date: date | None = None
    location: str | None = Field(default=None, max_length=255)  # college/university location
    description: str | None = Field(default=None)


class InvolvementCreate(InvolvementBase):
    pass


class InvolvementUpdate(SQLModel):
    role: str | None = Field(default=None, max_length=255)
    organization: str | None = Field(default=None, max_length=255)
    start_date: date | None = None
    end_date: date | None = None
    location: str | None = Field(default=None, max_length=255)
    description: str | None = Field(default=None)


class Involvement(InvolvementBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="user.id")
    user: "User" = Relationship(back_populates="involvements")


class InvolvementPublic(InvolvementBase):
    id: uuid.UUID
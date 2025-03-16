import uuid
from datetime import date
from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from .user import User


class EducationBase(SQLModel):
    degree: str = Field(max_length=255)
    qualification: str | None = Field(default=None, max_length=255)
    major: str = Field(max_length=255)
    institution: str = Field(max_length=255)
    location: str = Field(max_length=255)
    graduation_year: int
    minor: str | None = Field(default=None, max_length=255)
    gpa: float | None = Field(default=None)
    additional_info: str | None = Field(default=None)


class EducationCreate(EducationBase):
    pass


class EducationUpdate(SQLModel):
    degree: str | None = Field(default=None, max_length=255)
    qualification: str | None = Field(default=None, max_length=255)
    major: str | None = Field(default=None, max_length=255)
    institution: str | None = Field(default=None, max_length=255)
    location: str | None = Field(default=None, max_length=255)
    graduation_year: int | None = None
    minor: str | None = Field(default=None, max_length=255)
    gpa: float | None = Field(default=None)
    additional_info: str | None = Field(default=None)


class Education(EducationBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="user.id")
    user: "User" = Relationship(back_populates="educations")


class EducationPublic(EducationBase):
    id: uuid.UUID
    user_id: uuid.UUID
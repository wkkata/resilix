import uuid
from datetime import date
from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from .user import User


class ProjectBase(SQLModel):
    title: str = Field(max_length=255)
    organization: str = Field(max_length=255)
    start_date: date
    end_date: date | None = None
    project_url: str | None = Field(default=None, max_length=255)
    description: str | None = Field(default=None)


class ProjectCreate(ProjectBase):
    pass


class ProjectUpdate(SQLModel):
    title: str | None = Field(default=None, max_length=255)
    organization: str | None = Field(default=None, max_length=255)
    start_date: date | None = None
    end_date: date | None = None
    project_url: str | None = Field(default=None, max_length=255)
    description: str | None = Field(default=None)


class Project(ProjectBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="user.id")
    user: "User" = Relationship(back_populates="projects")


class ProjectPublic(ProjectBase):
    id: uuid.UUID
    user_id: uuid.UUID
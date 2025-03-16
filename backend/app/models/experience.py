import uuid
from datetime import date
from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel, Session, select

if TYPE_CHECKING:
    from .user import User


class ExperienceBase(SQLModel):
    role: str = Field(max_length=255)
    company: str = Field(max_length=255)
    start_date: date
    end_date: date | None = None
    location: str | None = Field(default=None, max_length=255)
    description: str | None = Field(default=None)


class ExperienceCreate(ExperienceBase):
    pass


class ExperienceUpdate(SQLModel):
    role: str | None = Field(default=None, max_length=255)
    company: str | None = Field(default=None, max_length=255)
    start_date: date | None = None
    end_date: date | None = None
    location: str | None = Field(default=None, max_length=255)
    description: str | None = Field(default=None)


class Experience(ExperienceBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="user.id")
    user: "User" = Relationship(back_populates="experiences")

    @classmethod
    def validate_date_overlap(cls, session: Session, user_id: uuid.UUID, start_date: date, end_date: date | None, exclude_id: uuid.UUID | None = None) -> bool:
        statement = select(Experience).where(Experience.user_id == user_id)
        if exclude_id:
            statement = statement.where(Experience.id != exclude_id)
        experiences = session.exec(statement).all()
        
        for exp in experiences:
            if end_date is None or exp.end_date is None:
                if start_date <= (exp.end_date or date.max) and (end_date or date.max) >= exp.start_date:
                    return False
            elif start_date <= exp.end_date and end_date >= exp.start_date:
                return False
        return True

class ExperiencePublic(ExperienceBase):
    id: uuid.UUID
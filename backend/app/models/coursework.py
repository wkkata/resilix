from datetime import datetime
from typing import Optional
import uuid

from sqlmodel import Field, SQLModel, Relationship

class CourseworkBase(SQLModel):
    course_name: str = Field(index=True)
    institution: str = Field(index=True)
    completion_date: datetime
    skill_learned: str
    skill_application: str

class Coursework(CourseworkBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="user.id")
    user: Optional["User"] = Relationship(back_populates="courseworks")

class CourseworkCreate(CourseworkBase):
    pass

class CourseworkUpdate(SQLModel):
    course_name: Optional[str] = None
    institution: Optional[str] = None
    completion_date: Optional[datetime] = None
    skill_learned: Optional[str] = None
    skill_application: Optional[str] = None

class CourseworkPublic(CourseworkBase):
    id: uuid.UUID
import uuid

from sqlmodel import Field, Relationship, SQLModel


# Shared properties
class SkillBase(SQLModel):
    content: str = Field(max_length=255)


# Properties to receive via API on creation
class SkillCreate(SkillBase):
    pass


# Properties to receive via API on update
class SkillUpdate(SkillBase):
    content: str | None = Field(default=None, max_length=255)  # type: ignore


# Database model
class Skill(SkillBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="user.id")
    user: "User" = Relationship(back_populates="skills")


# Properties to return via API
class SkillPublic(SkillBase):
    id: uuid.UUID
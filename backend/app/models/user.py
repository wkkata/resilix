import uuid

from typing import List, Optional

from pydantic import EmailStr
from sqlmodel import Field, Relationship, SQLModel

from .experience import Experience
from .education import Education
from .skill import Skill
from app.models.certificate import Certificate


# Shared properties
class UserBase(SQLModel):
    email: EmailStr = Field(unique=True, index=True, max_length=255)
    is_active: bool = True
    is_superuser: bool = False
    full_name: str | None = Field(default=None, max_length=255)
    country: str | None = Field(default=None, max_length=100)
    state: str | None = Field(default=None, max_length=100)
    phone_number: str | None = Field(default=None, max_length=20)
    personal_website: str | None = Field(default=None, max_length=255)
    linkedin_url: str | None = Field(default=None, max_length=255)
    show_on_resume: bool = Field(default=True)


# Properties to receive via API on creation
class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=40)


class UserRegister(SQLModel):
    email: EmailStr = Field(max_length=255)
    password: str = Field(min_length=8, max_length=40)
    full_name: str | None = Field(default=None, max_length=255)


# Properties to receive via API on update, all are optional
class UserUpdate(UserBase):
    email: EmailStr | None = Field(default=None, max_length=255)  # type: ignore
    password: str | None = Field(default=None, min_length=8, max_length=40)


class UserUpdateMe(SQLModel):
    full_name: str | None = Field(default=None, max_length=255)
    email: EmailStr | None = Field(default=None, max_length=255)
    phone_number: str | None = Field(default=None, max_length=20)
    personal_website: str | None = Field(default=None, max_length=255)
    linkedin_url: str | None = Field(default=None, max_length=255)
    show_on_resume: bool | None = Field(default=None)
    country: str | None = Field(default=None, max_length=100)
    state: str | None = Field(default=None, max_length=100)


class UpdatePassword(SQLModel):
    current_password: str = Field(min_length=8, max_length=40)


class NewPassword(SQLModel):
    token: str
    new_password: str = Field(min_length=8, max_length=40)


# Database model, database table inferred from class name
class User(UserBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    email: EmailStr = Field(unique=True, index=True)
    hashed_password: str = Field()
    is_active: bool = Field(default=True)
    is_superuser: bool = Field(default=False)
    items: List["Item"] = Relationship(back_populates="owner")
    experiences: List["Experience"] = Relationship(back_populates="user")
    educations: List["Education"] = Relationship(back_populates="user")
    projects: List["Project"] = Relationship(back_populates="user")
    skills: List["Skill"] = Relationship(back_populates="user")
    certificates: List["Certificate"] = Relationship(back_populates="user")
    courseworks: List["Coursework"] = Relationship(back_populates="user")


# Properties to return via API, id is always required
class UserPublic(UserBase):
    id: uuid.UUID


class UsersPublic(SQLModel):
    data: list[UserPublic]
    count: int
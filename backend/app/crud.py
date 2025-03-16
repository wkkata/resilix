import uuid
from typing import Any

from sqlmodel import Session, select

from app.core.security import get_password_hash, verify_password
from app.models import Item, ItemCreate, User, UserCreate, UserUpdate, Experience, ExperienceCreate, ExperienceUpdate, Education, EducationCreate, EducationUpdate, Project, ProjectCreate, ProjectUpdate


def create_user(*, session: Session, user_create: UserCreate) -> User:
    db_obj = User.model_validate(
        user_create, update={"hashed_password": get_password_hash(user_create.password)}
    )
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj


def update_user(*, session: Session, db_user: User, user_in: UserUpdate) -> Any:
    user_data = user_in.model_dump(exclude_unset=True)
    extra_data = {}
    if "password" in user_data:
        password = user_data["password"]
        hashed_password = get_password_hash(password)
        extra_data["hashed_password"] = hashed_password
    db_user.sqlmodel_update(user_data, update=extra_data)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


def get_user_by_email(*, session: Session, email: str) -> User | None:
    statement = select(User).where(User.email == email)
    session_user = session.exec(statement).first()
    return session_user


def authenticate(*, session: Session, email: str, password: str) -> User | None:
    db_user = get_user_by_email(session=session, email=email)
    if not db_user:
        return None
    if not verify_password(password, db_user.hashed_password):
        return None
    return db_user


def create_item(*, session: Session, item_in: ItemCreate, owner_id: uuid.UUID) -> Item:
    db_item = Item.model_validate(item_in, update={"owner_id": owner_id})
    session.add(db_item)
    session.commit()
    session.refresh(db_item)
    return db_item


def create_experience(*, session: Session, experience_in: ExperienceCreate, user_id: uuid.UUID) -> Experience:
    if not Experience.validate_date_overlap(session, user_id, experience_in.start_date, experience_in.end_date):
        raise ValueError("Experience dates overlap with existing experiences")
    db_experience = Experience.model_validate(experience_in, update={"user_id": user_id})
    session.add(db_experience)
    session.commit()
    session.refresh(db_experience)
    return db_experience

def get_experiences(*, session: Session, user_id: uuid.UUID) -> list[Experience]:
    statement = select(Experience).where(Experience.user_id == user_id)
    experiences = session.exec(statement).all()
    return experiences

def update_experience(*, session: Session, db_experience: Experience, experience_in: ExperienceUpdate) -> Experience:
    experience_data = experience_in.model_dump(exclude_unset=True)
    if "start_date" in experience_data or "end_date" in experience_data:
        start_date = experience_data.get("start_date", db_experience.start_date)
        end_date = experience_data.get("end_date", db_experience.end_date)
        if not Experience.validate_date_overlap(session, db_experience.user_id, start_date, end_date, db_experience.id):
            raise ValueError("Experience dates overlap with existing experiences")
    db_experience.sqlmodel_update(experience_data)
    session.add(db_experience)
    session.commit()
    session.refresh(db_experience)
    return db_experience

def delete_experience(*, session: Session, experience_id: uuid.UUID) -> None:
    statement = select(Experience).where(Experience.id == experience_id)
    experience = session.exec(statement).first()
    if experience:
        session.delete(experience)
        session.commit()


def create_education(*, session: Session, education_in: EducationCreate, user_id: uuid.UUID) -> Education:
    db_education = Education.model_validate(education_in, update={"user_id": user_id})
    session.add(db_education)
    session.commit()
    session.refresh(db_education)
    return db_education

def get_educations(*, session: Session, user_id: uuid.UUID) -> list[Education]:
    statement = select(Education).where(Education.user_id == user_id)
    educations = session.exec(statement).all()
    return educations

def update_education(*, session: Session, db_education: Education, education_in: EducationUpdate) -> Education:
    education_data = education_in.model_dump(exclude_unset=True)
    db_education.sqlmodel_update(education_data)
    session.add(db_education)
    session.commit()
    session.refresh(db_education)
    return db_education

def delete_education(*, session: Session, education_id: uuid.UUID) -> None:
    statement = select(Education).where(Education.id == education_id)
    education = session.exec(statement).first()
    if education:
        session.delete(education)
        session.commit()


def create_project(*, session: Session, project_in: ProjectCreate, user_id: uuid.UUID) -> Project:
    db_project = Project.model_validate(project_in, update={"user_id": user_id})
    session.add(db_project)
    session.commit()
    session.refresh(db_project)
    return db_project

def get_projects(*, session: Session, user_id: uuid.UUID) -> list[Project]:
    statement = select(Project).where(Project.user_id == user_id)
    projects = session.exec(statement).all()
    return projects

def update_project(*, session: Session, db_project: Project, project_in: ProjectUpdate) -> Project:
    project_data = project_in.model_dump(exclude_unset=True)
    db_project.sqlmodel_update(project_data)
    session.add(db_project)
    session.commit()
    session.refresh(db_project)
    return db_project

def delete_project(*, session: Session, project_id: uuid.UUID) -> None:
    statement = select(Project).where(Project.id == project_id)
    project = session.exec(statement).first()
    if project:
        session.delete(project)
        session.commit()

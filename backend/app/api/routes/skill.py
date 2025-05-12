import uuid
from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from app import crud
from app.api import deps
from app.models import Skill, SkillCreate, SkillUpdate, SkillPublic

router = APIRouter()

@router.post("/", response_model=SkillPublic)
def create_skill(
    *,
    session: Session = Depends(deps.get_session),
    skill_in: SkillCreate,
    current_user = Depends(deps.get_current_user),
) -> Any:
    """Create new skill."""
    skill = crud.create_skill(session=session, skill_in=skill_in, user_id=current_user.id)
    return skill

@router.get("/", response_model=list[SkillPublic])
def read_skills(
    *,
    session: Session = Depends(deps.get_session),
    current_user = Depends(deps.get_current_user),
) -> Any:
    """Retrieve skills."""
    skills = crud.get_skills(session=session, user_id=current_user.id)
    return skills

@router.put("/{skill_id}", response_model=SkillPublic)
def update_skill(
    *,
    session: Session = Depends(deps.get_session),
    skill_id: uuid.UUID,
    skill_in: SkillUpdate,
    current_user = Depends(deps.get_current_user),
) -> Any:
    """Update a skill."""
    # 修改这里：获取单个技能而不是所有技能
    skill = session.query(Skill).filter(Skill.id == skill_id, Skill.user_id == current_user.id).first()
    if not skill:
        raise HTTPException(
            status_code=404,
            detail="Skill not found",
        )
    skill = crud.update_skill(session=session, db_skill=skill, skill_in=skill_in)
    return skill

@router.delete("/{skill_id}")
def delete_skill(
    *,
    session: Session = Depends(deps.get_session),
    skill_id: uuid.UUID,
    current_user = Depends(deps.get_current_user),
) -> Any:
    """Delete a skill."""
    # 修改这里：获取单个技能而不是所有技能
    skill = session.query(Skill).filter(Skill.id == skill_id, Skill.user_id == current_user.id).first()
    if not skill:
        raise HTTPException(
            status_code=404,
            detail="Skill not found",
        )
    crud.delete_skill(session=session, skill_id=skill_id)
    return {"status": "success"}
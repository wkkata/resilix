from typing import List
import uuid  # 添加这一行导入uuid模块

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from app.api import deps
from app.models.coursework import Coursework, CourseworkCreate, CourseworkUpdate, CourseworkPublic
from app.models.user import User

router = APIRouter()

@router.post("/", response_model=CourseworkPublic)
async def create_coursework(
    *,
    db: Session = Depends(deps.get_session),
    coursework_in: CourseworkCreate,
    current_user: User = Depends(deps.get_current_user),
) -> Coursework:
    # 不使用from_orm方法，而是直接创建实例
    coursework = Coursework(
        course_name=coursework_in.course_name,
        institution=coursework_in.institution,
        completion_date=coursework_in.completion_date,
        skill_learned=coursework_in.skill_learned,
        skill_application=coursework_in.skill_application,
        user_id=current_user.id
    )
    db.add(coursework)
    db.commit()
    db.refresh(coursework)
    return coursework

@router.get("/", response_model=List[CourseworkPublic])
async def read_courseworks(
    *,
    db: Session = Depends(deps.get_session),
    current_user: User = Depends(deps.get_current_user),
) -> List[Coursework]:
    courseworks = db.query(Coursework).filter(Coursework.user_id == current_user.id).all()
    return courseworks

@router.get("/{coursework_id}", response_model=CourseworkPublic)
async def read_coursework(
    *,
    db: Session = Depends(deps.get_session),
    coursework_id: uuid.UUID,  # 修改为uuid.UUID类型
    current_user: User = Depends(deps.get_current_user),
) -> Coursework:
    coursework = db.query(Coursework).filter(Coursework.id == coursework_id, Coursework.user_id == current_user.id).first()
    if not coursework:
        raise HTTPException(status_code=404, detail="Coursework not found")
    return coursework

@router.put("/{coursework_id}", response_model=CourseworkPublic)
async def update_coursework(
    *,
    db: Session = Depends(deps.get_session),
    coursework_id: uuid.UUID,  # 修改为uuid.UUID类型
    coursework_in: CourseworkUpdate,
    current_user: User = Depends(deps.get_current_user),
) -> Coursework:
    coursework = db.query(Coursework).filter(Coursework.id == coursework_id, Coursework.user_id == current_user.id).first()
    if not coursework:
        raise HTTPException(status_code=404, detail="Coursework not found")
    
    update_data = coursework_in.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(coursework, field, value)
    
    db.add(coursework)
    db.commit()
    db.refresh(coursework)
    return coursework

@router.delete("/{coursework_id}")
async def delete_coursework(
    *,
    db: Session = Depends(deps.get_session),
    coursework_id: uuid.UUID,  # 修改为uuid.UUID类型
    current_user: User = Depends(deps.get_current_user),
) -> dict:
    coursework = db.query(Coursework).filter(Coursework.id == coursework_id, Coursework.user_id == current_user.id).first()
    if not coursework:
        raise HTTPException(status_code=404, detail="Coursework not found")
    
    db.delete(coursework)
    db.commit()
    return {"message": "Coursework deleted successfully"}
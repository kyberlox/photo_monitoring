from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database.database import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate, User as UserSchema

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/", response_model=list[UserSchema])
async def get_users(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User))
    users = result.scalars().all()
    return users


@router.get("/{user_id}", response_model=UserSchema)
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    return user


@router.post("/", response_model=UserSchema)
async def create_user(user_data: UserCreate, db: AsyncSession = Depends(get_db)):
    # Проверка на существование пользователя с таким именем (опционально)
    new_user = User(**user_data.model_dump())
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user


@router.put("/{user_id}", response_model=UserSchema)
async def update_user(
    user_id: int, user_data: UserUpdate, db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    
    update_data = user_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(user, field, value)
    
    await db.commit()
    await db.refresh(user)
    return user


@router.delete("/{user_id}")
async def delete_user(user_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    
    await db.delete(user)
    await db.commit()
    return {"message": "Пользователь удален"}
from pydantic import BaseModel
from typing import Optional


class UserBase(BaseModel):
    full_name: str
    is_admin: bool = False


class UserCreate(UserBase):
    pass


class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    is_admin: Optional[bool] = None


class User(UserBase):
    id: int

    class Config:
        from_attributes = True
from pydantic import BaseModel
from typing import Optional, List
from app.schemas.image import Image


class LocationBase(BaseModel):
    name: Optional[str] = None
    coord_x: float
    coord_y: float


class LocationCreate(LocationBase):
    pass


class LocationUpdate(BaseModel):
    name: Optional[str] = None
    coord_x: Optional[float] = None
    coord_y: Optional[float] = None


class Location(LocationBase):
    id: int
    images: List[Image] = []

    class Config:
        from_attributes = True
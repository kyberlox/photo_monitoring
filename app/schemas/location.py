from pydantic import BaseModel, Field
from typing import Optional, List
from app.schemas.media import Media


class LocationBase(BaseModel):
    name: Optional[str] = None
    coordinates: List[float] = Field(..., min_items=2, max_items=2, description="Координаты [x, y]")


class LocationCreate(LocationBase):
    pass


class LocationUpdate(BaseModel):
    name: Optional[str] = None
    coordinates: Optional[List[float]] = Field(None, min_items=2, max_items=2, description="Координаты [x, y]")


class Location(LocationBase):
    id: int
    # media: List[Media] = []  # временно отключено из-за проблем с асинхронной загрузкой

    class Config:
        from_attributes = True
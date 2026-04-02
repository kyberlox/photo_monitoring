from pydantic import BaseModel, Field
from typing import Optional, List
from app.schemas.photo import Photo


class LocationBase(BaseModel):
    name: Optional[str] = None
    coordinates: List[float] = Field(..., min_items=2, max_items=2, description="Координаты [x, y]")


# Схема для создания фото внутри локации (без location_id, т.к. он будет установлен автоматически)
class PhotoCreateForLocation(BaseModel):
    title: str
    comment: Optional[str] = None
    base64_data: Optional[str] = Field(None, description="Фото в формате base64")


class LocationCreate(LocationBase):
    photos: Optional[List[PhotoCreateForLocation]] = Field(
        None, description="Список фото для загрузки вместе с локацией"
    )


class LocationUpdate(BaseModel):
    name: Optional[str] = None
    coordinates: Optional[List[float]] = Field(None, min_items=2, max_items=2, description="Координаты [x, y]")


class Location(LocationBase):
    id: int
    photos: List[Photo] = []

    class Config:
        from_attributes = True
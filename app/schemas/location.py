from pydantic import BaseModel, Field
from typing import Optional, List
from app.schemas.media import Media, MediaType
from datetime import datetime


class LocationBase(BaseModel):
    name: Optional[str] = None
    coordinates: List[float] = Field(..., min_items=2, max_items=2, description="Координаты [x, y]")


# Схема для создания медиафайла внутри локации (без location_id, т.к. он будет установлен автоматически)
class MediaCreateForLocation(BaseModel):
    title: str
    comment: Optional[str] = None
    media_type: MediaType = MediaType.PHOTO
    base64_data: Optional[str] = Field(None, description="Фото/видео в формате base64")
    content: Optional[str] = Field(None, description="Текстовое описание (для media_type='text')")


class LocationCreate(LocationBase):
    media: Optional[List[MediaCreateForLocation]] = Field(
        None, description="Список медиафайлов для загрузки вместе с локацией"
    )


class LocationUpdate(BaseModel):
    name: Optional[str] = None
    coordinates: Optional[List[float]] = Field(None, min_items=2, max_items=2, description="Координаты [x, y]")


class Location(LocationBase):
    id: int
    # media: List[Media] = []  # временно отключено из-за проблем с асинхронной загрузкой

    class Config:
        from_attributes = True
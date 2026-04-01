from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum


class MediaType(str, Enum):
    PHOTO = "photo"
    VIDEO = "video"
    TEXT = "text"


class MediaBase(BaseModel):
    title: str
    comment: Optional[str] = None
    media_type: MediaType = MediaType.PHOTO


class MediaCreate(MediaBase):
    location_id: int
    # Для photo/video можно передать base64_data, для text - content
    base64_data: Optional[str] = Field(None, description="Фото/видео в формате base64")
    content: Optional[str] = Field(None, description="Текстовое описание (для media_type='text')")


class MediaUpdate(BaseModel):
    title: Optional[str] = None
    comment: Optional[str] = None
    base64_data: Optional[str] = Field(None, description="Новое фото/видео в base64")
    content: Optional[str] = Field(None, description="Новое текстовое описание")


class Media(MediaBase):
    id: int
    created_at: datetime
    file_path: Optional[str] = None  # путь к файлу (для photo/video)
    content: Optional[str] = None    # текстовое содержание (для text)
    location_id: int
    base64_data: Optional[str] = None  # будет заполнено при запросе для photo/video

    class Config:
        from_attributes = True
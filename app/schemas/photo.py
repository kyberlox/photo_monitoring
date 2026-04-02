from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class PhotoBase(BaseModel):
    title: str
    comment: Optional[str] = None
    # media_type удалён, т.к. только фото


class PhotoCreate(PhotoBase):
    location_id: int
    base64_data: Optional[str] = Field(None, description="Фото в формате base64")


class PhotoUpdate(BaseModel):
    title: Optional[str] = None
    comment: Optional[str] = None
    base64_data: Optional[str] = Field(None, description="Новое фото в base64")


class Photo(PhotoBase):
    id: int
    created_at: datetime
    file_path: Optional[str] = None  # путь к файлу
    location_id: int
    base64_data: Optional[str] = None  # будет заполнено при запросе

    class Config:
        from_attributes = True
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class ImageBase(BaseModel):
    title: str
    comment: Optional[str] = None


class ImageCreate(ImageBase):
    location_id: int
    author_id: int
    base64_data: str = Field(..., description="Изображение в формате base64")


class ImageUpdate(BaseModel):
    title: Optional[str] = None
    comment: Optional[str] = None
    base64_data: Optional[str] = Field(None, description="Новое изображение в base64 (опционально)")


class Image(ImageBase):
    id: int
    created_at: datetime
    file_path: str
    location_id: int
    author_id: int
    base64_data: Optional[str] = None  # будет заполнено при запросе

    class Config:
        from_attributes = True
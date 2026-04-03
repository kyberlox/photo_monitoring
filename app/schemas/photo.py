from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class PhotoBase(BaseModel):
    title: str
    comment: Optional[str] = None
    # media_type удалён, т.к. только фото


class PhotoCreate(PhotoBase):
    location_id: int
    # file будет передаваться как UploadFile в form-data, не как поле схемы


class PhotoUpdate(BaseModel):
    title: Optional[str] = None
    comment: Optional[str] = None
    # file будет передаваться как UploadFile в form-data, не как поле схемы


class Photo(PhotoBase):
    id: int
    created_at: datetime
    file_url: Optional[str] = None   # URL для доступа к файлу через статику
    location_id: int

    class Config:
        from_attributes = True
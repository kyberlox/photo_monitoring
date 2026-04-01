from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum

from app.database.database import Base


class MediaType(enum.Enum):
    PHOTO = "photo"
    VIDEO = "video"
    TEXT = "text"


class Media(Base):
    __tablename__ = "media"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    file_path = Column(String, nullable=True)  # путь к файлу (для photo/video)
    content = Column(Text, nullable=True)  # текстовое описание или base64 (для text)
    media_type = Column(Enum(MediaType, native_enum=False), nullable=False, default=MediaType.PHOTO)
    comment = Column(Text, nullable=True)  # дополнительный комментарий
    
    # Внешний ключ на локацию
    location_id = Column(Integer, ForeignKey("locations.id", ondelete="CASCADE"), nullable=False)
    
    # Связь
    location = relationship("Location", back_populates="media")
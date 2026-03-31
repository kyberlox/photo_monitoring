from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database.database import Base


class Image(Base):
    __tablename__ = "images"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    file_path = Column(String, nullable=False)  # путь к файлу на диске (обязательный)
    comment = Column(Text, nullable=True)  # комментарий к изображению
    
    # Внешние ключи
    author_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    location_id = Column(Integer, ForeignKey("locations.id", ondelete="CASCADE"), nullable=False)
    
    # Связи
    author = relationship("User", back_populates="images")
    location = relationship("Location", back_populates="images")
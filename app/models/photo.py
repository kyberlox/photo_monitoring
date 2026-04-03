from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database.database import Base


class Photo(Base):
    __tablename__ = "photos"

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    file_path = Column(String, nullable=True)  # путь к файлу
    comment = Column(Text, nullable=True)  # дополнительный комментарий
    
    # Внешний ключ на локацию
    location_id = Column(Integer, ForeignKey("locations.id", ondelete="CASCADE"), nullable=False)
    
    # Связь
    location = relationship("Location", back_populates="photos")
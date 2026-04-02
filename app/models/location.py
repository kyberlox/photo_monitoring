from sqlalchemy import Column, Integer, String, ARRAY, Float
from sqlalchemy.orm import relationship

from app.database.database import Base


class Location(Base):
    __tablename__ = "locations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=True)  # необязательное
    coordinates = Column(ARRAY(Float), nullable=False)  # [x, y]

    # Связь с фото
    photos = relationship("Photo", back_populates="location", cascade="all, delete-orphan")
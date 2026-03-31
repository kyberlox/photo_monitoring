from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship

from app.database.database import Base


class Location(Base):
    __tablename__ = "locations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=True)  # необязательное
    coord_x = Column(Float, nullable=False)
    coord_y = Column(Float, nullable=False)

    # Связь с изображениями
    images = relationship("Image", back_populates="location", cascade="all, delete-orphan")
from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship

from app.database.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=False)
    is_admin = Column(Boolean, default=False)

    # Связь с изображениями
    images = relationship("Image", back_populates="author", cascade="all, delete-orphan")
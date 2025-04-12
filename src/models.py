import enum
from sqlalchemy import Column, Integer, String, Enum, Float, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from src.database import Base


class UserStatus(enum.Enum):
    USER = 0
    ADMIN = 1


class ObjectCategory(enum.Enum):
    CAFE = "CAFE"
    CINEMA = "CINEMA"
    PARK = "PARK"


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_admin = Column(Enum(UserStatus), nullable=False, default=UserStatus.USER)
    access_token = Column(String, nullable=True)
    refresh_token = Column(String, nullable=True)

    comments = relationship("Comments", back_populates="user", cascade="all, delete-orphan")


class Objects(Base):
    __tablename__ = "object"

    id = Column(Integer, primary_key=True, index=True)
    address = Column(String, nullable=False)
    category = Column(Enum(ObjectCategory), nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    ramp = Column(Boolean, nullable=False, default=False)
    lowered_curb = Column(Boolean, nullable=False, default=False)
    tactile_marking = Column(Boolean, nullable=False, default=False)
    accessible_restroom = Column(Boolean, nullable=False, default=False)
    entrance = Column(Boolean, nullable=False, default=False)
    level_sidewalk = Column(Boolean, nullable=False, default=False)
    elevator = Column(Boolean, nullable=False, default=False)
    hoist = Column(Boolean, nullable=False, default=False)
    accessible_parking = Column(Boolean, nullable=False, default=False)

    comments = relationship("Comments", back_populates="object", cascade="all, delete-orphan")


class Comments(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    object_id = Column(Integer, ForeignKey("object.id"), nullable=False)
    text = Column(String, nullable=False)
    rating = Column(Float, nullable=False)

    user = relationship("Users", back_populates="comments")
    object = relationship("Objects", back_populates="comments")

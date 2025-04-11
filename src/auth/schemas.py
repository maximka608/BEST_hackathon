from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, constr, ConfigDict

from src.models import UserStatus


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserLoginResponse(BaseModel):
    access_token: str
    refresh_token: str


class UserResponse(BaseModel):
    username: str
    email: EmailStr
    is_admin: UserStatus

    model_config = ConfigDict(from_attributes=True)


class UserProfileResponse(BaseModel):
    username: str
    email: str

    model_config = ConfigDict(from_attributes=True)


class AdminResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    is_admin: UserStatus
    access_token: Optional[str]
    refresh_token: Optional[str]

    model_config = ConfigDict(from_attributes=True)

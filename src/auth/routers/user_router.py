from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.auth.schemas import UserProfileResponse, UserResponse
from src.database import get_db
from src.models import Users
from src.utils.auth_services import get_current_user

user_router = APIRouter()


@user_router.get("/", response_model=UserResponse)
def profile(user: Users = Depends(get_current_user)):
    """User can view his profile information"""
    return UserResponse.model_validate(user, from_attributes=True)


@user_router.delete("/")
def delete_user(user: Users = Depends(get_current_user), db: Session = Depends(get_db)):
    """Allow user to delete their account"""
    db.delete(user)
    db.commit()

    return {"message": "User deleted"}
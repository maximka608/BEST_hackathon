from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.auth.hashing import verify_password
from src.auth.schemas import UserResponse, UserCreate, UserLogin, UserLoginResponse
from src.database import get_db
from src.utils.exceptions import (
    email_already_registered_exception,
    username_already_registered_exception,
    invalid_credentials_exception,
    invalid_token_exception,
    user_not_found_exception
)
from src.utils.getters_services import get_user_by_email, get_user_by_username, get_user_by_id
from src.utils.jwt_handlers import create_refresh_token, create_access_token, decode_access_token
from src.utils.services import update_user_tokens, create_user

auth_router = APIRouter()


@auth_router.post("/signup", response_model=UserResponse)
def sign_up(user: UserCreate, db: Session = Depends(get_db)):
    """Register a new user"""
    existing_user = get_user_by_email(db, user.email)
    if existing_user:
        raise email_already_registered_exception

    existing_user = get_user_by_username(db, user.username)
    if existing_user:
        raise username_already_registered_exception

    new_user = create_user(db, user)
    return new_user


@auth_router.post("/signin")
def sign_in(user: UserLogin, db: Session = Depends(get_db)):
    db_user = get_user_by_email(db, user.email)
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise invalid_credentials_exception

    access_token = create_access_token(data={"sub": str(db_user.id)})
    refresh_token = create_refresh_token(data={"sub": str(db_user.id)})

    update_user_tokens(db, db_user.id, access_token, refresh_token)

    return UserLoginResponse(access_token=access_token, refresh_token=refresh_token)


@auth_router.patch("/logout")
def logout(token: dict = Depends(decode_access_token), db: Session = Depends(get_db)):
    """Allow user to logout"""
    if not token:
        raise invalid_token_exception

    user_id = int(token.get("sub"))

    user = get_user_by_id(db, user_id)

    if not user:
        raise user_not_found_exception

    user.access_token = None
    user.refresh_token = None
    db.commit()

    return {"message": "User logged out"}

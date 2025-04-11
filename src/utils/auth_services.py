from fastapi import Depends
from sqlalchemy.orm import Session

from src.auth.hashing import verify_password
from src.database import get_db
from src.models import UserStatus
from src.utils.exceptions import user_not_admin_exception, invalid_token_exception, user_not_found_exception
from src.utils.getters_services import get_user_by_email, get_user_by_id
from src.utils.jwt_handlers import decode_access_token


def authenticate_user(db: Session, email: str, password: str):
    """Check user and his password"""
    user = get_user_by_email(db, email)

    if not user or not verify_password(password, user.hashed_password):
        return None

    return user


def get_current_user(token: dict = Depends(decode_access_token), db: Session = Depends(get_db)):
    """Check if token exists and return user"""
    if not token:
        raise invalid_token_exception

    user_id = int(token.get("sub"))
    user = get_user_by_id(db, user_id)
    if not user:
        raise user_not_found_exception

    return user


def get_current_admin(token: dict = Depends(decode_access_token), db: Session = Depends(get_db)):
    """Перевірити чи є токен та чи він адмінський"""
    if not token:
        raise invalid_token_exception

    admin_id = int(token.get("sub"))

    if not is_user_admin(db, admin_id):
        raise user_not_admin_exception

    return db


def is_user_admin(db: Session, user_id: int):
    user = get_user_by_id(db, user_id)
    return user.is_admin == UserStatus.ADMIN

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.hashing import verify_password
from src.database import get_db
from src.models import UserStatus
from src.utils.exceptions import user_not_admin_exception, invalid_token_exception, user_not_found_exception
from src.utils.getters_services import get_user_by_email, get_user_by_id
from src.utils.jwt_handlers import decode_access_token


async def authenticate_user(db: AsyncSession, email: str, password: str):
    """Check user and his password"""
    user = await get_user_by_email(db, email)

    if not user or not verify_password(password, user.hashed_password):
        return None

    return user


async def get_current_user(token: dict = Depends(decode_access_token), db: AsyncSession = Depends(get_db)):
    """Check if token exists and return user"""
    if not token:
        raise invalid_token_exception

    user_id = int(token.get("sub"))
    user = await get_user_by_id(db, user_id)
    if not user:
        raise user_not_found_exception

    return user


async def get_current_admin(token: dict = Depends(decode_access_token), db: AsyncSession = Depends(get_db)):
    """Перевірити чи є токен та чи він адмінський"""
    if not token:
        raise invalid_token_exception

    admin_id = int(token.get("sub"))

    if not await is_user_admin(db, admin_id):
        raise user_not_admin_exception

    return db


async def get_current_bot_or_admin(token: dict = Depends(decode_access_token), db: AsyncSession = Depends(get_db)):
    """Перевірити чи є токен та чи він ботським"""
    if not token:
        raise invalid_token_exception

    admin_id = int(token.get("sub"))
    if not await is_user_bot(db, admin_id) and not await is_user_admin(db, admin_id):
        raise user_not_admin_exception

    return db


async def is_user_admin(db: AsyncSession, user_id: int):
    user = await get_user_by_id(db, user_id)
    return user.is_admin == UserStatus.ADMIN and user.is_approved_by_admin


async def is_user_bot(db: AsyncSession, user_id: int):
    user = await get_user_by_id(db, user_id)
    return user.is_admin == UserStatus.BOT and user.is_approved_by_admin

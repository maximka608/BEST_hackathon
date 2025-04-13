from datetime import datetime, timezone

from sqlalchemy.orm import Session

from src.auth.hashing import hash_password
from src.auth.schemas import UserCreate
from src.models import Users, UserStatus
from src.utils.getters_services import get_user_by_id



def create_user(db: Session, user: UserCreate):
    """New user creation"""
    hashed_password = hash_password(user.password)

    new_user = Users(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password,
        is_admin=UserStatus.USER,
    )
    db.add(new_user)
    db.flush()
    db.commit()
    db.refresh(new_user)
    return new_user

def update_user_tokens(db: Session, user_id: int, new_access_token: str, new_refresh_token: str):
    """Update the tokens of an existing user, after login"""
    actual_user = get_user_by_id(db, user_id)

    if not actual_user:
        return None

    actual_user.access_token = new_access_token
    actual_user.refresh_token = new_refresh_token
    actual_user.updated_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(actual_user)
    return actual_user
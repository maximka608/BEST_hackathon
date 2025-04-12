from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.auth.schemas import AdminResponse
from src.models import UserStatus
from src.utils.auth_services import get_current_admin
from src.utils.exceptions import user_not_found_exception, user_is_max_rank_exception, user_is_min_rank_exception
from src.utils.getters_services import get_user_by_id

admin_router = APIRouter()


@admin_router.patch("/promotion/{user_id}", response_model=AdminResponse)
def promotion(user_id: int, db: Session = Depends(get_current_admin)):
    """Make a user an admin"""
    user = get_user_by_id(db, user_id)

    if not user:
        raise user_not_found_exception

    if user.is_admin == UserStatus.ADMIN:
        raise user_is_max_rank_exception

    user.is_admin = UserStatus(user.is_admin.value + 1)
    db.commit()
    db.refresh(user)
    return AdminResponse.model_validate(user)


@admin_router.patch("/demotion/{user_id}", response_model=AdminResponse)
def demotion(user_id: int, db: Session = Depends(get_current_admin)):
    """Make a user an admin"""
    user = get_user_by_id(db, user_id)

    if not user:
        raise user_not_found_exception

    if user.is_admin == UserStatus.USER:
        raise user_is_min_rank_exception

    user.is_admin = UserStatus(user.is_admin.value - 1)
    db.commit()
    db.refresh(user)
    return AdminResponse.model_validate(user)
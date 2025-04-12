from sqlalchemy import select
from sqlalchemy.orm import Session

from src.models import Users, Objects


def get_user_by_id(db: Session, user_id: int):
    return (db.execute(select(Users).where(Users.id == user_id))).scalars().first()


def get_user_by_email(db: Session, email: str):
    return (db.execute(select(Users).where(Users.email == email))).scalars().first()


def get_user_by_username(db: Session, username: str):
    return (db.execute(select(Users).where(Users.username == username))).scalars().first()

def get_all_objects(db: Session):
    return (db.execute(select(Objects))).scalars().all()
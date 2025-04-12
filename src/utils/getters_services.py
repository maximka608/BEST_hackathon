from sqlalchemy import select
from sqlalchemy.orm import Session
from src.models import Users
from src.models import Objects
from sqlalchemy import or_

def get_user_by_id(db: Session, user_id: int):
    return (db.execute(select(Users).where(Users.id == user_id))).scalars().first()

def get_user_by_email(db: Session, email: str):
    return (db.execute(select(Users).where(Users.email == email))).scalars().first()

def get_user_by_username(db: Session, username: str):
    return (db.execute(select(Users).where(Users.username == username))).scalars().first()

def filter_wheelchair_accessible(db: Session, category: str):
    results = db.query(Objects).filter(Objects.category == category,
        or_(Objects.ramp == 1,
        Objects.entrance == 1,
        Objects.accessible_restroom == 1,
        Objects.level_sidewalk == 1,
        Objects.elevator == 1,
        Objects.hoist == 1,
        Objects.accessible_parking == 1
        )).all()
    return results

def filter_visually_impaired(db: Session, category: str):
    results = db.query(Objects).filter( Objects.category == category,
        or_(Objects.tactile_marking == 1,
        Objects.lowered_curb == 1)
        ).all()

    return results
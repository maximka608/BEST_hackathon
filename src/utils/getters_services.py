from sqlalchemy import select
from sqlalchemy.orm import Session

from sqlalchemy import or_
from src.models import Users, Objects, Comments


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

def get_all_objects(db: Session):
    return (db.execute(select(Objects))).scalars().all()


def get_all_from_mongols(db: Session):
    query_nodes_ways = {
        "type": {"$in": ["node", "way"]},
        "$or": [
            {"tags.wheelchair": {"$exists": True}},
            {"tags.toilets_wheelchair": {"$exists": True}},
            {"tags.tactile_paving": {"$exists": True}},
            {"tags.amenity": {"$exists": True}},
            {"tags.tourism": {"$exists": True}},
            {"tags.office": {"$exists": True}},
        ]
    }
    nodes = list(db["osm_collection"].find(query_nodes_ways))
    return nodes


def get_comments_by_object_id(object_id: str, db: Session):
    return (db.execute(select(Comments).where(Comments.object_id == object_id, Comments.text != None))).scalars().all()



def get_ratings_by_object_id(object_id: str, db: Session):
    return (db.execute(select(Comments).where(Comments.object_id == object_id, Comments.rating != None))).scalars().all()



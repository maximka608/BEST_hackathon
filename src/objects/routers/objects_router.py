from pyexpat.errors import messages

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.database import get_db
from src.db.mongo import db, get_mongo_db, serialize_object_id
from src.utils.getters_services import get_all_objects, get_all_from_mongols

object_router = APIRouter()

@object_router.get("/")
def get_objects_list(db: Session = Depends(get_db)):
    objects = get_all_objects(db)
    return objects


@object_router.get("/nodes")
def get_all_the_mongols(db: Session = Depends(get_mongo_db)):
    nodes = get_all_from_mongols(db)

    if not nodes:
        return {"message": "No nodes found"}

    serialized_nodes = serialize_object_id(nodes)

    return {"message": "Mongols are here", "nodes": serialized_nodes}


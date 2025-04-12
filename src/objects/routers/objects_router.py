from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.database import get_db
from src.utils.getters_services import get_all_objects

object_router = APIRouter()

@object_router.get("/")
def get_objects_list(db: Session = Depends(get_db)):
    objects = get_all_objects(db)
    return objects


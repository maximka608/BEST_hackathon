from fastapi import APIRouter, Depends, Body
from sqlalchemy.orm import Session

from src.models import Objects
from src.objects.schemas import ObjectUpdate, ObjectResponse
from src.utils.auth_services import get_current_admin
from src.utils.exceptions import object_not_found_exception

admin_objects_router = APIRouter()


@admin_objects_router.patch("/{object_id}", response_model=ObjectResponse)
def update_object(object_id: int, updates: ObjectUpdate = Body(...), db: Session = Depends(get_current_admin)):
    obj = db.query(Objects).filter(Objects.id == object_id).first()
    if not obj:
        raise object_not_found_exception

    update_data = updates.dict(exclude_unset=True)

    for field, value in update_data.items():
        if hasattr(obj, field):
            setattr(obj, field, value)

    db.commit()
    db.refresh(obj)
    return ObjectResponse.model_validate(obj, from_attributes=True)
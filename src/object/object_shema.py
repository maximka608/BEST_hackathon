from pydantic import BaseModel
from typing import Optional

class ObjectResponse(BaseModel):
    id: int
    category: str
    ramp: Optional[int] = None
    entrance: Optional[int] = None
    accessible_restroom: Optional[int] = None
    level_sidewalk: Optional[int] = None
    elevator: Optional[int] = None
    hoist: Optional[int] = None
    accessible_parking: Optional[int] = None
    tactile_marking: Optional[int] = None
    lowered_curb: Optional[int] = None

    class Config:
        orm_mode = True
from typing import Optional

from pydantic import BaseModel, ConfigDict


class ObjectResponse(BaseModel):
    id: int
    address: str
    latitude: float
    longitude: float
    ramp: bool
    lowered_curb: bool
    tactile_marking: bool
    accessible_parking: bool
    accessible_restroom: bool
    entrance: bool
    level_sidewalk: bool
    elevator: bool
    hoist: bool
    accessible_parking: bool

    model_config = ConfigDict(from_attributes=True)



class ObjectUpdate(BaseModel):
    ramp: Optional[bool] = None
    lowered_curb: Optional[bool] = None
    tactile_marking: Optional[bool] = None
    accessible_parking: Optional[bool] = None
    accessible_restroom: Optional[bool] = None
    entrance: Optional[bool] = None
    level_sidewalk: Optional[bool] = None
    elevator: Optional[bool] = None
    hoist: Optional[bool] = None
    accessible_parking: Optional[bool] = None
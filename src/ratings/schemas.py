from pydantic import BaseModel, ConfigDict


class RatingCreate(BaseModel):
    object_id: str
    rating: float

class RatingResponse(BaseModel):
    object_id: str
    rating: float

    model_config = ConfigDict(from_attributes=True)
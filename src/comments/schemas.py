from typing import Optional

from pydantic import BaseModel, ConfigDict

class CommentCreate(BaseModel):
    object_id: str
    text: Optional[str] = None
    rating: Optional[float] = None

class CommentResponse(BaseModel):
    user_id: int
    object_id: str
    text: str
    rating: Optional[float] = None

    model_config = ConfigDict(from_attributes=True)


class RatingResponse(BaseModel):
    user_id: int
    object_id: str
    text: Optional[str] = None
    rating: float

    model_config = ConfigDict(from_attributes=True)


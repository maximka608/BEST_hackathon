from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.database import get_db
from src.models import Ratings, Users
from src.ratings.schemas import RatingResponse
from src.utils.auth_services import get_current_admin
from src.utils.exceptions import user_not_found_exception, user_is_max_rank_exception, user_is_min_rank_exception

ratings_router = APIRouter()

@ratings_router.post("/", response_model=RatingResponse)
def create_rating(rating: RatingResponse, user: Users = Depends(get_current_admin), db: Session = Depends(get_db)):
    new_rating = Ratings(
        object_id=rating.object_id,
        rating=rating.rating
    )
    db.add(new_rating)
    db.commit()
    db.refresh(new_rating)

    return RatingResponse.model_validate(new_rating, from_attributes=True)


@ratings_router.get("/{object_id}", response_model=RatingResponse)
def get_rating_by_object_id(object_id: str, db: Session = Depends(get_db)):
    rating = db.query(Ratings).filter(Ratings.object_id == object_id).first()
    if not rating:
        user_not_found_exception


    return RatingResponse.model_validate(rating, from_attributes=True)

@ratings_router.patch("/{object_id}", response_model=RatingResponse)
def update_rating(object_id: str, rating: float, user: Users = Depends(get_current_admin), db: Session = Depends(get_db)):
    existing_rating = db.query(Ratings).filter(Ratings.object_id == object_id).first()
    if not existing_rating:
        user_not_found_exception

    existing_rating.rating = rating
    db.commit()
    db.refresh(existing_rating)

    return RatingResponse.model_validate(existing_rating, from_attributes=True)

@ratings_router.patch("/increase/{object_id}", response_model=RatingResponse)
def increase_rating(object_id: str, user: Users = Depends(get_current_admin), db: Session = Depends(get_db)):
    existing_rating = db.query(Ratings).filter(Ratings.object_id == object_id).first()
    if not existing_rating:
        user_not_found_exception

    if existing_rating.rating >= 5:
        raise user_is_max_rank_exception


    existing_rating.rating += 0.5
    if existing_rating.rating > 5:
        existing_rating.rating = 5
    db.commit()
    db.refresh(existing_rating)

    return RatingResponse.model_validate(existing_rating, from_attributes=True)

@ratings_router.patch("/decrease/{object_id}", response_model=RatingResponse)
def decrease_rating(object_id: str, user: Users = Depends(get_current_admin), db: Session = Depends(get_db)):
    existing_rating = db.query(Ratings).filter(Ratings.object_id == object_id).first()
    if not existing_rating:
        user_not_found_exception

    if existing_rating.rating <= 0:
        raise user_is_min_rank_exception

    existing_rating.rating -= 0.5
    if existing_rating.rating < 0:
        existing_rating.rating = 0
    db.commit()
    db.refresh(existing_rating)

    return RatingResponse.model_validate(existing_rating, from_attributes=True)
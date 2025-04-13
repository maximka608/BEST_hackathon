from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.comments.schemas import CommentResponse, RatingResponse, CommentCreate
from src.database import get_db
from src.models import Users
from src.utils.auth_services import get_current_user
from src.utils.exceptions import comments_must_provide_text_or_rating_exception
from src.utils.getters_services import get_comments_by_object_id, get_ratings_by_object_id
from src.utils.services import create_comment

comments_router = APIRouter()

@comments_router.post("/comments", response_model=CommentResponse)
def add_comment(comment: CommentCreate, user: Users = Depends(get_current_user), sqlite_db: Session = Depends(get_db)):

    if not comment.text and not comment.rating:
        raise comments_must_provide_text_or_rating_exception
    new_comment = create_comment(user, comment, sqlite_db)
    return new_comment

@comments_router.get("/comments/{object_id}", response_model=List[CommentResponse])
def get_comments(object_id: str,
                 sqlite_db: Session = Depends(get_db)):

    comments = get_comments_by_object_id(object_id=object_id, db=sqlite_db)
    if not comments:
        return {"message": "No comments found"}

    return [CommentResponse.model_validate(comment) for comment in comments]


@comments_router.get("/ratings/{object_id}", response_model=List[RatingResponse])
def get_ratings(object_id: str, sqlite_db: Session = Depends(get_db)):

    comments = get_ratings_by_object_id(object_id=object_id, db=sqlite_db)
    if not comments:
        return {"message": "No comments found"}

    return [RatingResponse.model_validate(comment) for comment in comments]
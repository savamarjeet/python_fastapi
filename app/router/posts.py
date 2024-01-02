from app import schemas
from fastapi import APIRouter
from app import models
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.auth_bearer import JWTBearer
from app.utils import get_pagination_params, get_db_session

router = APIRouter()

# Create a new post endpoint
@router.post('/')
def create_post(post: schemas.Post, logged_user_id = Depends(JWTBearer()), db: Session = Depends(get_db_session)):
    new_post = models.Post(**post.__dict__, author_id=logged_user_id)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return {"message": "Post created successfully"}


# List posts endpoint
@router.get('/', response_model = list[schemas.DetailPost])
def list_posts(logged_user_id = Depends(JWTBearer()), db: Session = Depends(get_db_session), pagination: dict = Depends(get_pagination_params)):
    start = pagination["skip"]
    end = start + pagination["limit"]

    # Query active posts based on pagination
    db_post = db.query(models.Post).filter(models.Post.is_active == True)
    return db_post[start:end]


# list all post done by logged in author
@router.get("/author-post", response_model = list[schemas.AuthorPost])
def author_post(user_id = Depends(JWTBearer()), db: Session = Depends(get_db_session), pagination: dict = Depends(get_pagination_params)):
    start = pagination["skip"]
    end = start + pagination["limit"]

    db_post = db.query(models.Post).filter(models.Post.author_id == user_id)
    if not db_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No Post Found for Author")
    return db_post[start:end]


# Get post by ID endpoint
@router.get('/{post_id}', response_model = schemas.DetailPost)
def posts(post_id: int, logged_user_id = Depends(JWTBearer()), db: Session = Depends(get_db_session)):
    # Query post by ID and check if it's active
    db_post = db.query(models.Post).filter(models.Post.id == post_id, models.Post.is_active == True).first()
    # check if the post exists
    if not db_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    return db_post



# Delete post by ID endpoint
@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int, logged_user_id = Depends(JWTBearer()), db: Session = Depends(get_db_session)):
    db_post = db.query(models.Post).filter(models.Post.id == post_id).first()

    # check if the post exists
    if not db_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    
    # soft delete, make record inactive
    db_post.is_active = False
    db.commit()
    db.refresh(db_post)

    return {"message": "Post Deleted Successfully"}


@router.patch("/{post_id}", response_model = schemas.DetailPost)
def update_post(post_id: int, update_post: schemas.Post, user_id = Depends(JWTBearer()), db: Session = Depends(get_db_session)):
    db_post = db.query(models.Post).filter(models.Post.id == post_id, models.Post.is_active == True).first()
    
    # check if the post exists
    if not db_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

    for key, value in update_post.__dict__.items():
        setattr(db_post, key, value)

    db.commit()
    db.refresh(db_post)

    return db_post


from app import schemas
from app import models
from app.models import User
from app.database import Base, engine, SessionLocal
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from . import app
from app.utils import create_access_token, create_refresh_token, verify_password, get_hashed_password
from app.auth_bearer import JWTBearer
from app.utils import get_pagination_params

Base.metadata.create_all(engine)

def get_db_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()

@app.post("/register")
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db_session)):
    existing_user = db.query(models.User).filter_by(email=user.email).first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")

    encrypted_password = get_hashed_password(user.password)

    new_user = models.User(username=user.username, email=user.email, password=encrypted_password, address=user.address)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "User created successfully"}


@app.post('/login', response_model=schemas.TokenSchema)
def login(request: schemas.Requestdetails, db: Session = Depends(get_db_session)):
    user = db.query(User).filter(User.email == request.email, User.is_active == True).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect email")
    hashed_pass = user.password
    if not verify_password(request.password, hashed_pass):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect password"
        )
    
    access = create_access_token(user.id)
    refresh = create_refresh_token(user.id)

    token_db = models.TokenTable(user_id=user.id,  access_token=access,  refresh_token=refresh, status=True)
    db.add(token_db)
    db.commit()
    db.refresh(token_db)
    return {
        "access_token": access,
        "refresh_token": refresh,
    }


@app.post('/logout')
def logout(token_user_id = Depends(JWTBearer()), db: Session = Depends(get_db_session)):
    user_id = token_user_id
    db.query(models.TokenTable).filter(models.TokenTable.user_id == user_id).delete()
    db.commit()
    return {"message":"Logout Successfully"} 


@app.get('/users', response_model = list[schemas.UserBase])
def list_users(token_user_id = Depends(JWTBearer()), db: Session = Depends(get_db_session), pagination: dict = Depends(get_pagination_params)):
    start = pagination["skip"]
    end = start + pagination["limit"]

    user = db.query(models.User).filter(models.User.is_active == True)
    return user[start:end]


def get_user(user_id: int, db: Session = Depends(get_db_session)):
    user = db.query(models.User).filter(models.User.id == user_id, models.User.is_active == True).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


@app.get('/users/{user_id}', response_model = schemas.UserDetail)
def get_user(user_id: int, token_user_id = Depends(JWTBearer()), user: models.User = Depends(get_user)):
    return user


@app.post('/posts')
def create_post(post: schemas.Post, logged_user_id = Depends(JWTBearer()), db: Session = Depends(get_db_session)):
    new_post = models.Post(**post.__dict__, author_id=logged_user_id)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return {"message": "Post created successfully"}


@app.get('/posts', response_model = list[schemas.DetailPost])
def list_posts(logged_user_id = Depends(JWTBearer()), db: Session = Depends(get_db_session), pagination: dict = Depends(get_pagination_params)):
    start = pagination["skip"]
    end = start + pagination["limit"]

    db_post = db.query(models.Post).filter(models.Post.is_active == True)
    return db_post[start:end]


@app.get('/posts/{post_id}', response_model = schemas.DetailPost)
def posts(post_id: int, logged_user_id = Depends(JWTBearer()), db: Session = Depends(get_db_session)):
    db_post = db.query(models.Post).filter(models.Post.id == post_id, models.Post.is_active == True).first()
    # check if the post exists
    if not db_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    return db_post


@app.delete("/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int, db: Session = Depends(get_db_session)):
    db_post = db.query(models.Post).filter(models.Post.id == post_id).first()

    # check if the post exists
    if not db_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    
    # soft delete, make record inactive
    db_post.is_active = False
    db.commit()
    db.refresh(db_post)

    return {"message": "Post Deleted Successfully"}


@app.patch("/posts/{post_id}", response_model = schemas.DetailPost)
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


@app.get("/author-post", response_model = list[schemas.AuthorPost])
def author_post(user_id = Depends(JWTBearer()), db: Session = Depends(get_db_session), pagination: dict = Depends(get_pagination_params)):
    start = pagination["skip"]
    end = start + pagination["limit"]

    db_post = db.query(models.Post).filter(models.Post.author_id == user_id)
    if not db_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No Post Found for Author")
    return db_post[start:end]

from app import schemas
from fastapi import APIRouter
from app import models
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.auth_bearer import JWTBearer
from app.utils import get_pagination_params, get_db_session

router = APIRouter()

# List users endpoint
@router.get('/', response_model = list[schemas.UserBase])
def list_users(token_user_id = Depends(JWTBearer()), db: Session = Depends(get_db_session), pagination: dict = Depends(get_pagination_params)):
    start = pagination["skip"]
    end = start + pagination["limit"]

    # Query active users based on pagination
    user = db.query(models.User).filter(models.User.is_active == True)
    return user[start:end]


# Get user by ID endpoint
def get_user(user_id: int, db: Session = Depends(get_db_session)):
    user = db.query(models.User).filter(models.User.id == user_id, models.User.is_active == True).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


# Get user details by ID endpoint
@router.get('/{user_id}', response_model = schemas.UserDetail)
def get_user(user_id: int, token_user_id = Depends(JWTBearer()), user: models.User = Depends(get_user)):
    return user

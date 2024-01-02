from app import schemas
from fastapi import APIRouter
from app import models
from app.models import User
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.utils import create_access_token, create_refresh_token, verify_password, get_hashed_password
from app.auth_bearer import JWTBearer
from app.utils import get_db_session

router = APIRouter()

@router.get("/register")
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


# Login endpoint
@router.post('/login', response_model=schemas.TokenSchema)
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

    # Generate access and refresh tokens
    access = create_access_token(user.id)
    refresh = create_refresh_token(user.id)

    # Store tokens in the database
    token_db = models.TokenTable(user_id=user.id,  access_token=access,  refresh_token=refresh, status=True)
    db.add(token_db)
    db.commit()
    db.refresh(token_db)
    return {
        "access_token": access,
        "refresh_token": refresh,
    }


# Logout endpoint
@router.post('/logout')
def logout(user_id = Depends(JWTBearer()), db: Session = Depends(get_db_session)):
    db.query(models.TokenTable).filter(models.TokenTable.user_id == user_id).delete()
    db.commit()
    return {"message":"Logout Successfully"}

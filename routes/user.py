from fastapi import APIRouter, Depends, HTTPException, status
from config.bd import SessionLocal
from sqlalchemy.orm import Session

# USERS
from schemas.user import (UserCreate, UserResponse, UserLogin)
from services.user_services import UserService

router = APIRouter(tags=["Users"])

def get_db():
    db= SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/create_user")
def create_user(user_data: UserCreate, db: Session = Depends(get_db)):
    try:
        user_service = UserService(db)

        user = user_service.create_user(
            user_data=user_data,
            creator_id = 1#user_data['id_user_create']
        )
        return user

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail= "Failed to create user"
        )

@router.post("/login")
def login(user_data: UserLogin, db: Session = Depends(get_db)):
    try:
        user_service = UserService(db)

        token_response = user_service.login(user_data=user_data)

        return token_response
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail= "Failed to login"
        )
from fastapi import APIRouter, Depends, HTTPException, status
from config.bd import SessionLocal
from sqlalchemy.orm import Session
from models.user import User

from schemas.notifications import (NotificationCreate, NotificationResponse)
from services.notification_service import NotificationRepository
from .dependencies import get_current_user

router = APIRouter(tags=["Notifications"])

def get_db():
    db= SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/channels")
def get_channels(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):

    notification_repo = NotificationRepository(db)
    channels = notification_repo.available_channels
    
    return channels
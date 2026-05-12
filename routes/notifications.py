from fastapi import APIRouter, Depends, HTTPException, status
from config.bd import SessionLocal
from sqlalchemy.orm import Session

from schemas.notifications import (NotificationCreate, NotificationResponse)
from services.notification_service import NotificationRepository

router = APIRouter(tags=["Notifications"])

def get_db():
    db= SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/channels")
def get_channels(db: Session = Depends(get_db)):

    notification_repo = NotificationRepository(db)
    channels = notification_repo.available_channels
    
    return channels
from fastapi import FastAPI, Depends, HTTPException, status
from config.bd import SessionLocal
from sqlalchemy.orm import Session

# USERS
from routes import (user, notifications)

app = FastAPI(
    title="Notification System"
)

app.include_router(
    user.router,
    prefix='/api/user')

app.include_router(
    notifications.router,
    prefix="/api/notifications"
)
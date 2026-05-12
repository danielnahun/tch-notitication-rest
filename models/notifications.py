from sqlalchemy import Column, Integer, String, Text, Boolean, TIMESTAMP,Enum
from config.bd import Base

class Notificaciones(Base):
    __tablename__ = 'notifications'
    id_notification = Column(Integer, primary_key=True, autoincrement=True)
    sender_id = Column(Integer)
    receiver_id = Column(Integer)
    subject = Column(String(255), nullable=False)
    message = Column(Text)
    channel = Column(
        Enum('email','sms','push', name='channel_notification'),
        nullable=False,
        default='email'
    )
    status = Column(
        Enum('pending','sent','failed'),
        nullable=False,
        default='pending'
    )
    created_by = Column(Integer)
    created_at = Column(TIMESTAMP, nullable=False)
    deleted_by = Column(Integer)
    deleted_at = Column(TIMESTAMP, nullable=True)
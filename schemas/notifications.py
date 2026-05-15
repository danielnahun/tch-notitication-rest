from enum import Enum
from datetime import datetime
from pydantic import BaseModel, ConfigDict
from typing import Optional

class NotificationChannel(str, Enum):
    EMAIL = 'email'
    SMS = 'sms'
    PUSH = 'push'

class NotificationStatus(str, Enum):
    PENDING = 'pending'
    SENT = 'sent'
    FAILED = 'failed'

class NotificationBase(BaseModel):
    sender_id: int
    receiver_id: int
    subject: str
    message: str
    status: NotificationStatus = NotificationStatus.PENDING
    model_config = ConfigDict(from_attributes=True, use_enum_values=True)

class NotificationCreate(NotificationBase):
    created_at: datetime
    sender_contact: Optional[str] = None
    receiver_contact: Optional[str] = None

class NotificationCreateMail(NotificationCreate):
    receiver_contact: str
    sender_contact: str

class NotificationCreateNumber(NotificationCreate):
    receiver_contact: str
    sender_contact: str

class NotificationResponse(NotificationBase):
    id_notification: int
    channel: NotificationChannel
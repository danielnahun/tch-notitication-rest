from enum import Enum
from datetime import datetime
from pydantic import BaseModel, ConfigDict

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
    channel: NotificationChannel
    status: NotificationStatus = NotificationStatus.PENDING
    model_config = ConfigDict(from_attributes=True, use_enum_values=True)

class NotificationCreate(NotificationBase):
    created_by: datetime

class NotificationResponse(NotificationBase):
    id_notification: int
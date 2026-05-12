from typing import Dict, List, Optional
from sqlalchemy.orm import Session
from .channels_service import(
    BaseNotificationChannel,
    EmailChannel,
    SMSChannel,
    PushChannel
)
from schemas.notifications import NotificationChannel

class NotificationRepository:

    def __init__(self, db:Session):
        self.db = db
        self._channels: Dict[str, BaseNotificationChannel] = {
            NotificationChannel.EMAIL : EmailChannel(),
            NotificationChannel.SMS : SMSChannel(),
            NotificationChannel.PUSH : PushChannel()
        }
    
    @property
    def available_channels(self) -> List[str]:
        return list(self._channels.keys())

    def get_channel(self, channel: NotificationChannel):
        return self._channels.get(channel)

from schemas.notifications import NotificationCreate, NotificationChannel
from sqlalchemy.orm import Session
from abc import ABC, abstractmethod

class BaseNotificationChannel(ABC):
    def __init__(self, channel_name:str):
        self._channel_name = channel_name

    @property
    def channel_name(self) -> str:
        return self._channel_name

    @abstractmethod
    def send(self, notification: NotificationCreate) -> bool:
        ...

    def _log(self, notification: NotificationCreate, success: bool) -> None:
        state = "enviada" if success else "fallida"
        print(
            f"[{self._channel_name.upper()}] {state} | "
            f"De user#{notification.sender_id} -> user#{notification.receiver_id} | "
            f"Asunto: {notification.subject}"
        )

class EmailChannel(BaseNotificationChannel):
    def __init__(self):
        super().__init__(NotificationChannel.EMAIL)
    
    def send(self, notification: NotificationCreate) -> bool:
        success = True
        self._log(notification, success)
        return success

class SMSChannel(BaseNotificationChannel):
    def __init__(self):
        super().__init__(NotificationChannel.SMS)
    
    def send(self, notification: NotificationCreate) -> bool:
        success = True
        self._log(notification, success)
        return success

class PushChannel(BaseNotificationChannel):
    def __init__(self):
        super().__init__(NotificationChannel.PUSH)
    
    def send(self, notification: NotificationCreate) -> bool:
        success = True
        self._log(notification, success)
        return success
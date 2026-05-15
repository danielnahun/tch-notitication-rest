from schemas.notifications import (
    NotificationCreate, 
    NotificationChannel,
    NotificationCreateMail,
    NotificationCreateNumber
)
from sqlalchemy.orm import Session
from abc import ABC, abstractmethod
from pydantic import validate_email

class BaseNotificationChannel(ABC):
    def __init__(self, channel_name:str, db: Session):
        self._channel_name = channel_name
        self.db = db

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
            f"Contacto emisor: {notification.sender_contact} | "
            f"Contacto receptor: {notification.receiver_contact} | "
            f"Asunto: {notification.subject}"
        )

class EmailChannel(BaseNotificationChannel):
    def __init__(self, db):
        super().__init__(NotificationChannel.EMAIL, db)
    
    def send(self, notification: NotificationCreateMail) -> bool:
        if not self._validate_email(notification.receiver_contact) or not self._validate_email(notification.sender_contact):
            self._log(notification, False)
            return False
        
        print(f"Email enviado a {notification.receiver_contact} de {notification.sender_contact}")
        self._log(notification, True)
        return True
    
    def _validate_email(self, email: str) -> bool:
        return validate_email(email)

class BaseNumberChannel(BaseNotificationChannel):
    def __init__(self, channel_name:str, db: Session):
        super().__init__(channel_name, db)
    
    def _validate_number(self, number: str) -> bool:
        if not number.isdigit():
            return False
        
        return True

class SMSChannel(BaseNumberChannel):
    def __init__(self, db): 
        super().__init__(NotificationChannel.SMS, db)
    
    def send(self, notification: NotificationCreateNumber) -> bool:
        if not self._validate_number(notification.receiver_contact) or not self._validate_number(notification.sender_contact):
            self._log(notification, False)
            return False
        
        print(f"SMS enviado a {notification.receiver_contact} de {notification.sender_contact}")
        self._log(notification, True)
        return True

class PushChannel(BaseNumberChannel):
    def __init__(self, db):
        super().__init__(NotificationChannel.PUSH, db)
    
    def send(self, notification: NotificationCreateNumber) -> bool:
        if not self._validate_number(notification.receiver_contact) or not self._validate_number(notification.sender_contact):
            self._log(notification, False)
            return False
        
        print(f"Push enviado a {notification.receiver_contact} de {notification.sender_contact}")
        self._log(notification, True)
        return True
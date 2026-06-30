from typing import Dict, List, Optional
from sqlalchemy.orm import Session
from .channels_service import(
    BaseNotificationChannel,
    EmailChannel,
    SMSChannel,
    PushChannel
)
from models.user import User
from models.notifications import Notificaciones
from schemas.notifications import NotificationChannel, NotificationCreate, NotificationCreateMail, NotificationCreateNumber
from datetime import datetime, timedelta, timezone
from fastapi import HTTPException, status


class NotificationRepository:

    def __init__(self, db:Session):
        self.db = db
        self._channels: Dict[str, BaseNotificationChannel] = {
            NotificationChannel.EMAIL : EmailChannel(db),
            NotificationChannel.SMS : SMSChannel(db),
            NotificationChannel.PUSH : PushChannel(db)
        }
    
    @property
    def available_channels(self) -> List[str]:
        return list(self._channels.keys())

    def get_channel(self, channel: NotificationChannel):
        return self._channels.get(channel)

    def validate_receiver_user(self, user_id: int) -> Optional[User]:
        user = self.db.query(User).filter(User.id_user == user_id).first()
        return user

    def send_notification(self, noti_data: NotificationCreate, creator_user: User, channel:str):
        db = self.db

        if not self.validate_receiver_user(noti_data.receiver_id):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Usuario receptor inválido: {noti_data.receiver_id}")

        channel = self.get_channel(channel)

        if not channel:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Canal de notificación inválido: {channel}")

        if channel.channel_name == NotificationChannel.EMAIL:
            noti_data.sender_contact = creator_user.user_name
            noti = NotificationCreateMail(**noti_data.model_dump())
        elif channel.channel_name in (NotificationChannel.SMS, NotificationChannel.PUSH):
            noti = NotificationCreateNumber(**noti_data.model_dump())
        else:
            raise ValueError(f"Canal de notificación inválido: {channel}")

        success = channel.send(noti)

        if not success:
            raise ValueError(f"No se pudo enviar la notificación por el canal {channel.channel_name}")
        else:
            noti_dict = Notificaciones(
                sender_id = creator_user.id_user,
                receiver_id = noti_data.receiver_id,
                sender_contact = noti_data.sender_contact,
                receiver_contact = noti_data.receiver_contact,
                subject = noti_data.subject,
                message = noti_data.message,
                status = "sent",
                created_by = creator_user.id_user,
                channel = channel.channel_name,
                created_at = datetime.now(timezone.utc)
            )

            db.add(noti_dict)
            db.commit()
            db.refresh(noti_dict)

            return noti_dict


        

        


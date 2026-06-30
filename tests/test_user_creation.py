import pytest
from schemas.user import UserCreate
from services.user_services import UserService
from sqlalchemy import text
from models.user import User
import re
from werkzeug.security import check_password_hash
from datetime import datetime, timezone, timedelta

class TestUserCreation:

    def test_create_user(self, db_session):

        # Valores de prueba
        user_name = "test@example.com"
        user_password = "SecurePass2026"

        # Validacion de formato de correo
        self.validate_mail(user_name)

        # Creacion Usuario
        user_data = UserCreate(
            user_name = user_name,
            user_password = user_password
        )
        service = UserService(db_session)
        user = service.create_user(user_data, id_user_create=1)
        now = datetime.now(timezone.utc)

        # Consulta a BD sobre usuario creado
        result = self.search_user_create_in_bd(db_session, user_name)
        assert result is not None

        # Verificacion de Password (3 validaciones)

        stored_password = result['user_password']

        assert stored_password != user_password
        assert stored_password.startswith("pbkdf2:sha256:"), f"La password hasheada es: {stored_password}"
        assert check_password_hash(stored_password, user_password)

        # Verificar formato de created_at, zona horaria comparada con BD

        created_at  = result['created_at']

        assert created_at is not None
        assert isinstance(created_at, datetime)
        if created_at.tzinfo is None:
            created_at = created_at.replace(tzinfo=timezone.utc)
            diff = abs((now-created_at).total_seconds())
            assert diff < 60, f"La fecha no es reciente: diff={diff}s"

        # Ultima validacion de formatos en BD ( 5 validaciones)

        assert result['user_name'] == user_name
        assert result['is_active'] in (True, 1, 1.0)
        assert result['created_by'] == 1
        assert result['token'] is not None
        assert len(result['token']) > 0


    def validate_mail(self, user_name):
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        assert re.match(email_regex, user_name)

    def search_user_create_in_bd(self, db_session, user_name):
        """Query directa a BD por si el commit falla"""
        return db_session.execute(
            text("SELECT * FROM user WHERE user_name = :email"),
            {"email": user_name}
        ).mappings().first()

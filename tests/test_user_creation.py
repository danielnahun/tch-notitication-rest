import pytest
from schemas.user import UserCreate
from services.user_services import UserService
from sqlalchemy import text
from models.user import User
import re
from werkzeug.security import check_password_hash
from datetime import datetime, timezone, timedelta

@pytest.fixture
def create_user(db_session):
    """Crea un usuario y retorna los valores de la creacion"""
    user_data = UserCreate(
        user_name = "test@example.com",
        user_password = "SecurePass123"
    )
    service = UserService(db_session)
    service.create_user(user_data, id_user_create=1)

    result = db_session.execute(
        text("SELECT * FROM user WHERE user_name = :email"),
        {"email": "test@example.com"}
    ).mappings().first()

    return result


class TestUserCreation:

    def test_validate_mail(self, create_user):
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        assert re.match(email_regex, create_user['user_name'])

    def test_user_created_in_bd(self, create_user):
        assert create_user is not None

    def test_time_in_created(self, create_user):
        now = datetime.now(timezone.utc)
        created = create_user['created_at']
        if created.tzinfo is None:
            created = created.replace(tzinfo=timezone.utc)
        diff = abs((now - created).total_seconds())
        assert diff < 60

    def test_check_password_hashed(self, create_user):
        stored_password = create_user['user_password']
        assert stored_password.startswith("pbkdf2:sha256:")
        assert check_password_hash(stored_password, "SecurePass123")

    def test_formats_in_bd_validate(self, create_user):
        assert create_user['user_name'] == "test@example.com"
        assert create_user['is_active'] in (True, 1, 1.0)
        assert create_user['created_by'] == 1
        assert create_user['token'] is not None
        assert len(create_user['token']) > 0
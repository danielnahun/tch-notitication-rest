import pytest
from jose import jwt
from sqlalchemy import text
import os
from dotenv import load_dotenv
load_dotenv()

from schemas.user import UserLogin
from models.user import User
from services.user_services import UserService

mock_user = {
    "user_name": "admin@test.com",
    "user_password": "hashed_admin"
}

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

@pytest.fixture
def user_login(db_session):
    """Primero resetea la contraseña a una real, y hace login"""
    service = UserService(db_session)
    user_data = UserLogin(
        user_name = mock_user['user_name'],
        user_password = mock_user['user_password']
    )
    service.reset_password(user_data)

    user_loged = service.login(user_data)
    return user_loged

class TestUserLogin:

    def test_login_succesfull(self, user_login):
        assert user_login['access_token'] is not None

    def test_validate_access_token(self, user_login):
        token_data = jwt.decode(user_login['access_token'], SECRET_KEY, algorithms=ALGORITHM)
        assert token_data['username'] == mock_user['user_name']
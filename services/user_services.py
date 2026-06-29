import os
from werkzeug.security import generate_password_hash, check_password_hash
from cryptography.fernet import Fernet
from schemas.user import UserCreate, UserLogin
from models.user import User
import secrets
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from jose import JWTError, jwt
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY", "123456")
ALGORITHM = os.getenv("ALGORITHM", "HS256")

class UserService:
    def __init__(self, db:Session):
        self.db = db

    def create_user(self, user_data: UserCreate, id_user_create:int):
        db = self.db

        existing_user = self.get_by_user_name(user_data.user_name)
        if existing_user:
            print(f"Usuario con username={user_data.user_name} ya existe")
            raise

        hashed_password = generate_password_hash(user_data.user_password)
        token = secrets.token_urlsafe(48)
        current_time = datetime.now()

        user_dict =  User(
            user_password = hashed_password,
            token = token,
            user_name = user_data.user_name,
            created_by = id_user_create,
            created_at = current_time
        )
        # try:
        db.add(user_dict)
        db.commit()
        db.refresh(user_dict)
        # except Exception as e:
        #     raise e

        return user_dict
    
    def get_by_user_name(self, username: str):
        db = self.db
        query = db.query(User).filter(User.user_name == username)
        return query.first()

    def get_by_token(self, token:str):
        db = self.db
        query = db.query(User).filter(User.token == token)
        return query.first()

    def login(self, user_data:UserLogin):
        db = self.db

        existing_user = self.get_by_user_name(user_data.user_name)
        if not existing_user:
            print(f"Usuario invalido")
            raise

        verify_password = check_password_hash(existing_user.user_password, user_data.user_password)
        if not verify_password:
            print("Contraseña invalida")
            raise

        token_data = {
            "sub": str(existing_user.id_user), 
            "username":existing_user.user_name,
            "iat": datetime.now(),
            "type": "access",
            "exp": datetime.now()+timedelta(hours=1)
            }

        access_token = jwt.encode(token_data, SECRET_KEY, algorithm=ALGORITHM)

        return{
            "access_token": access_token,
            "token_type": "bearer",
            "user":{
                "id": existing_user.id_user,
                "username": existing_user.user_name
            }
        }

    def reset_password(self,  user_data: UserCreate,):
        db = self.db

        user = self.get_by_user_name(user_data.user_name)
        if not user:
            print(f"Usuario invalido")
            raise

        hashed_password = generate_password_hash(user_data.user_password)
        token = secrets.token_urlsafe(48)
        current_time = datetime.now()

        user.user_password = hashed_password,
        user.token = token
        # try:
        db.commit()
        db.refresh(user_dict)
        # except Exception as e:
        #     raise e

        return user_dict



        









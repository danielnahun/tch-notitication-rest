import os
from fastapi import Depends, HTTPException, status, Header
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from jose import JWTError, jwt

from config.bd import get_db
from models.user import User
from dotenv import load_dotenv

load_dotenv()

security = HTTPBearer

SECRET_KEY = os.getenv("SECRET_KEY", "123456")
ALGORITHM = os.getenv("ALGORITHM", "HS256")

def get_current_user(
    credentials: HTTPAuthorizationCredentials= Depends(security),
    db: Session = Depends(get_db)
) -> User:
    try:
        token = credentials.credentials
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if expected_type and payload.get("type") != expected_type:
            raise JWTError("Token invalido")
        user_id = payload.get("sub")
        if user_id is None:
            print("Token invalido, user no encontrado")
            raise
        user = db.query(User).filter(User.id_user == int(user_id)).first()
        if user is None:
            print("Usuario no encontrado")
            raise
        return user

    except JWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No se validaron las credenciales",
            headers={"WWW-Authenticate": "Bearer"}
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Error Autenticacion",
            headers={"WWW-Authenticate": "Bearer"}
        )
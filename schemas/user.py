from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict, EmailStr

class UserBase(BaseModel):
    user_name: EmailStr = Field(min_length=1,description="Este campo debe ser tipo email")
    model_config = ConfigDict(from_attributes=True)

class UserCreate(UserBase):
    user_password: str = Field(min_length=5)
    id_user_create: int = Field(description="Relacion a Usuario creador")
    model_config = ConfigDict(from_attributes=True)

class UserLogin(UserBase):
    user_password: str = Field(min_length=5)
    model_config = ConfigDict(from_attributes=True)

class UserResponse(UserBase):
    id_user: int
    token: str = Field(min_length=1)
    is_active: bool
    created_by: int
    created_at: datetime
    deleted_by: int
    deleted_at: datetime
    model_config = ConfigDict(from_attributes=True)

from sqlalchemy import Column, Integer, String, Text, Boolean, TIMESTAMP
from config.bd import Base, engine

class User(Base):
    __tablename__ = 'user'
    id_user = Column(Integer, primary_key=True, autoincrement=True)
    user_name = Column(String(255), nullable=False)
    user_password = Column(String(255), nullable=False)
    token = Column(Text, nullable=True)
    is_active = Column(Boolean)
    created_by = Column(Integer)
    created_at = Column(TIMESTAMP, nullable=False)
    deleted_by = Column(Integer)
    deleted_at = Column(TIMESTAMP, nullable=True)

Base.metadata.create_all(bind=engine)
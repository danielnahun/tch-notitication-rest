import pytest
import os
from pathlib import Path
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

# Salvaguarda para no tocar BD real
os.environ["APP_ENV"] = ".env.test"

from config.bd import Base, get_db, engine
from main import app
from routes.dependencies import get_current_user
from models.user import User
from datetime import datetime

SEEDS_FILE = Path(__file__).parent.parent / "docker" / "init" / "002_seeds.sql"

@pytest.fixture(scope="session")
def setup_database(engine):
    """
    Crea tablas + carga datos
    Borrar todo al finalizar
    """
    Base.metadata.create_all(bind=engine)

    with engine.connect() as conn:
        seed_sql = SEEDS_FILE.read_text()
        for statement in seed_sql.split(";"):
            stmt = statement.strip()
            if stmt:
                from sqlalchemy import text
                conn.execute(text(stmt))
        conn.commit()
    
    yield engine

    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def db_session(setup_database):
    """
    Sesion real de BD, con rollback al finalizar.
    """
    connection = setup_database.connect()
    transaction = connection.begin()
    session = sessionmaker(bind=connection)()

    yield session

    session.close()
    transaction.rollback()
    connection.close()

@pytest.fixture
def mock_user():
    return User(
        id_user=1,
        user_name="admin@test.com",
        user_password="hashed_admin",
        token="token_admin",
        is_active=True,
        created_by=1,
        created_at=datetime.now(timezone.utc)
    )

@pytest.fixture
def client(db_session, mock_user):
    def override_db():
        yield db_session

    def override_current_user():
        return mock_user

    from routes.user import get_db as user_get_db
    from routes.notifications import get_db as notif_get_db
    from config.bd import get_db as config_get_db

    app.dependency_overrides[user_get_db] = override_db
    app.dependency_overrides[notif_get_db] = override_db
    app.dependency_overrides[config_get_db] = override_db
    app.dependency_overrides[get_current_user] = override_current_user

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()
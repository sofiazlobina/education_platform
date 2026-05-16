import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.core.deps import get_db
from app.models.user import User
from app.core.security import get_password_hash
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Создаём тестовую БД в памяти (SQLite)
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Фикстура для создания тестовой БД
@pytest.fixture(scope="function")
def db_session():
    # Создаём все таблицы
    from app.core.database import Base
    Base.metadata.create_all(bind=engine)
    
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        # Очищаем БД после теста
        Base.metadata.drop_all(bind=engine)

# Фикстура для подмены базы данных в приложении
@pytest.fixture(scope="function")
def client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()

# Тест регистрации
def test_register_user(client):
    response = client.post(
        "/api/v1/auth/register",
        json={
            "username": "testuser",
            "password": "testpass123",
            "first_name": "Test",
            "last_name": "User"
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["username"] == "testuser"
    assert data["first_name"] == "Test"
    assert "hashed_password" not in data  # Пароль не должен возвращаться

# Тест входа
def test_login_user(client, db_session):
    # Создаём пользователя
    user = User(
        username="loginuser",
        hashed_password=get_password_hash("password123"),
        is_active=True
    )
    db_session.add(user)
    db_session.commit()
    
    # Пробуем войти
    response = client.post(
        "/api/v1/auth/login",
        data={
            "username": "loginuser",
            "password": "password123"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

# Тест неверного пароля
def test_login_wrong_password(client, db_session):
    user = User(
        username="wrongpassuser",
        hashed_password=get_password_hash("correctpass"),
        is_active=True
    )
    db_session.add(user)
    db_session.commit()
    
    response = client.post(
        "/api/v1/auth/login",
        data={
            "username": "wrongpassuser",
            "password": "wrongpass"
        }
    )
    assert response.status_code == 401
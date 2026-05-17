import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.core.deps import get_db
from app.models.user import User
from app.core.security import get_password_hash
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Делаю тестовую SQLite базу
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Фикстура под тестовую БД
@pytest.fixture(scope="function")
def db_session():
    # Создаю все таблицы перед тестом
    from app.core.database import Base
    Base.metadata.create_all(bind=engine)
    
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        # После теста чищу БД
        Base.metadata.drop_all(bind=engine)

# Подменяю базу данных в приложении для тестов
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

# Проверка регистрации
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
    assert "hashed_password" not in data  # Пароль наружу не отдаем

# Проверка входа
def test_login_user(client, db_session):
    # Создаю пользователя
    user = User(
        username="loginuser",
        hashed_password=get_password_hash("password123"),
        is_active=True
    )
    db_session.add(user)
    db_session.commit()
    
    # Пытаюсь войти
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

# Проверка неверного пароля
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
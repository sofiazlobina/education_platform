import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.core.deps import get_db
from app.models.user import User
from app.models.course import Course
from app.core.security import get_password_hash
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def db_session():
    from app.core.database import Base
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

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

@pytest.fixture
def admin_token(client, db_session):
    # Создаём админа
    admin = User(
        username="admin",
        hashed_password=get_password_hash("adminpass"),
        is_active=True,
        is_superuser=True
    )
    db_session.add(admin)
    db_session.commit()
    
    # Логинимся
    response = client.post(
        "/api/v1/auth/login",
        data={"username": "admin", "password": "adminpass"}
    )
    return response.json()["access_token"]

def test_create_course(client, admin_token, db_session):
    headers = {"Authorization": f"Bearer {admin_token}"}
    response = client.post(
        "/api/v1/admin/courses",
        json={
            "title": "Test Course",
            "description": "Test Description"
        },
        headers=headers
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test Course"
    assert data["id"] == 1

def test_list_courses(client, db_session):
    # Создаём тестовый курс
    course = Course(title="Course 1", description="Desc 1")
    db_session.add(course)
    db_session.commit()
    
    response = client.get("/api/v1/student/courses")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["title"] == "Course 1"
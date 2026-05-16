from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from app.core.config import get_settings

settings = get_settings()

# connect_args нужен специально для SQLite
engine = create_engine(settings.DATABASE_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# ОПРЕДЕЛЕНИЕ БАЗЫ (Создаём пустой подкласс)
class Base(DeclarativeBase):
    pass
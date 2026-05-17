from sqlalchemy import Column, Integer, String, Text, JSON
from app.core.database import Base

class Test(Base):
    __tablename__ = "tests"

    id = Column(Integer, primary_key=True, index=True)
    question = Column(Text, nullable=False)
    options = Column(JSON, nullable=False)  # Список вариантов ответа
    correct_answer = Column(String(255), nullable=False)  # Тут хранится правильный ответ
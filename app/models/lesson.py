from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class Lesson(Base):
    __tablename__ = "lessons"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    content = Column(Text, nullable=True)  # Основной текст урока
    
    # Внешний ключ, урок привязан к курсу
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    
    # Связи между моделями
    course = relationship("Course", back_populates="lessons")
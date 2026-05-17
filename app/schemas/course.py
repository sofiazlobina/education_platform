from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from app.schemas.lesson import LessonResponse  # Импорт тут, чтобы не словить циклический импорт

# Что админ отправляет при создании курса
class CourseCreate(BaseModel):
    title: str
    description: Optional[str] = None

# Что приходит при обновлении курса
class CourseUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None

# Что возвращаем клиенту
class CourseResponse(BaseModel):
    id: int
    title: str
    description: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)
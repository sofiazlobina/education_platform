from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from app.schemas.lesson import LessonResponse  # импортируем позже

# Схема для создания курса (что принимает админ)
class CourseCreate(BaseModel):
    title: str
    description: Optional[str] = None

# Схема для обновления курса
class CourseUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None

# Схема ответа (что отдаём клиенту)
class CourseResponse(BaseModel):
    id: int
    title: str
    description: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)
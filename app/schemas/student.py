from pydantic import BaseModel, ConfigDict
from typing import Optional, List

# Ответ для курса (упрощённый для студента)
class CourseStudentResponse(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    
    model_config = ConfigDict(from_attributes=True)

# Ответ для урока
class LessonStudentResponse(BaseModel):
    id: int
    title: str
    content: str
    course_id: int
    
    model_config = ConfigDict(from_attributes=True)

# Ответ для теста (БЕЗ правильного ответа!)
class TestStudentResponse(BaseModel):
    id: int
    question: str
    options: List[str]
    # correct_answer скрыт от студента
    
    model_config = ConfigDict(from_attributes=True)

# Запрос на ответ теста
class TestAnswerSubmit(BaseModel):
    answer: str

# Результат проверки теста
class TestResultResponse(BaseModel):
    test_id: int
    is_correct: bool
    correct_answer: Optional[str] = None  # Показываем только если ответ неверный
    
    model_config = ConfigDict(from_attributes=True)

# Мой курс с прогрессом
class MyCourseResponse(BaseModel):
    course: CourseStudentResponse
    progress: float  # 0.0 - 100.0
    
    model_config = ConfigDict(from_attributes=True)

# Съема прогресса курса
class CourseProgressResponse(BaseModel):
    course_id: int
    course_title: str
    progress: float
    total_tests_passed: int = 0  # Заглушка, можно доработать позже
    
    model_config = ConfigDict(from_attributes=True)

from datetime import datetime

class TestResultHistory(BaseModel):
    test_id: int
    question: str
    your_answer: str
    is_correct: bool
    submitted_at: datetime

    model_config = ConfigDict(from_attributes=True)
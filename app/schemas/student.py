from pydantic import BaseModel, ConfigDict
from typing import Optional, List

# Ответ по курсу, урезанный для студента
class CourseStudentResponse(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    
    model_config = ConfigDict(from_attributes=True)

# Ответ по уроку
class LessonStudentResponse(BaseModel):
    id: int
    title: str
    content: str
    course_id: int
    
    model_config = ConfigDict(from_attributes=True)

# Ответ по тесту без правильного варианта
class TestStudentResponse(BaseModel):
    id: int
    question: str
    options: List[str]
    # correct_answer прячем от студента
    
    model_config = ConfigDict(from_attributes=True)

# Запрос с ответом на тест
class TestAnswerSubmit(BaseModel):
    answer: str

# Результат проверки ответа
class TestResultResponse(BaseModel):
    test_id: int
    is_correct: bool
    correct_answer: Optional[str] = None  # Показываем только если студент ошибся
    
    model_config = ConfigDict(from_attributes=True)

# Курс пользователя с прогрессом
class MyCourseResponse(BaseModel):
    course: CourseStudentResponse
    progress: float  # Диапазон прогресса 0.0 - 100.0
    
    model_config = ConfigDict(from_attributes=True)

# Схема прогресса курса
class CourseProgressResponse(BaseModel):
    course_id: int
    course_title: str
    progress: float
    total_tests_passed: int = 0  # Пока заглушка, потом можно допилить
    
    model_config = ConfigDict(from_attributes=True)

from datetime import datetime

class TestResultHistory(BaseModel):
    test_id: int
    question: str
    your_answer: str
    is_correct: bool
    submitted_at: datetime

    model_config = ConfigDict(from_attributes=True)

class GeneratedTestQuestion(BaseModel):
    question: str
    options: List[str]
    correct_answer: str
    source_lesson_id: Optional[int] = None


class PersonalTestGenerateRequest(BaseModel):
    course_id: int
    questions_count: int = 5


class PersonalTestGenerateResponse(BaseModel):
    course_id: int
    based_on_lessons: List[int]
    questions: List[GeneratedTestQuestion]

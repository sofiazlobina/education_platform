from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.deps import get_db, get_current_user
from app.models.course import Course
from app.models.lesson import Lesson
from app.models.test import Test
from app.models.user import User
from app.models.user_course import UserCourse
from app.schemas.student import (
    CourseStudentResponse,
    LessonStudentResponse,
    TestStudentResponse,
    TestAnswerSubmit,
    TestResultResponse,
    MyCourseResponse,
    CourseProgressResponse
)
from app.models.test_result import UserTestResult
from app.schemas.student import TestResultHistory

router = APIRouter(prefix="/api/v1/student", tags=["Student"])

# 1. Каталог всех курсов
@router.get("/courses", response_model=list[CourseStudentResponse])
def get_courses(db: Session = Depends(get_db)):
    return db.query(Course).all()

# 2. Детали курса + список уроков
@router.get("/courses/{course_id}", response_model=dict)
def get_course_details(course_id: int, db: Session = Depends(get_db)):
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Курс не найден")
    
    lessons = db.query(Lesson).filter(Lesson.course_id == course_id).all()
    return {
        "course": CourseStudentResponse.model_validate(course),
        "lessons": [LessonStudentResponse.model_validate(l) for l in lessons]
    }

# 3. Получить конкретный урок
@router.get("/lessons/{lesson_id}", response_model=LessonStudentResponse)
def get_lesson(lesson_id: int, db: Session = Depends(get_db)):
    lesson = db.query(Lesson).filter(Lesson.id == lesson_id).first()
    if not lesson:
        raise HTTPException(status_code=404, detail="Урок не найден")
    return lesson

# 4. Получить тест (без ответа)
@router.get("/tests/{test_id}", response_model=TestStudentResponse)
def get_test(test_id: int, db: Session = Depends(get_db)):
    test = db.query(Test).filter(Test.id == test_id).first()
    if not test:
        raise HTTPException(status_code=404, detail="Тест не найден")
    return test

# 🔹 НОВОЕ: Записаться на курс
@router.post("/courses/{course_id}/enroll", status_code=status.HTTP_201_CREATED)
def enroll_course(
    course_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Курс не найден")
    
    # Проверяем, не записан ли уже
    exists = db.query(UserCourse).filter(
        UserCourse.user_id == current_user.id,
        UserCourse.course_id == course_id
    ).first()
    if exists:
        raise HTTPException(status_code=400, detail="Вы уже записаны на этот курс")
    
    enrollment = UserCourse(user_id=current_user.id, course_id=course_id, progress=0.0)
    db.add(enrollment)
    db.commit()
    return {"message": f"Вы успешно записались на курс '{course.title}'"}

# 🔹 ОБНОВЛЁННОЕ: Отправить ответ на тест с сохранением прогресса
@router.post("/tests/{test_id}/submit", response_model=TestResultResponse)
def submit_test_answer(
    test_id: int,
    answer_data: TestAnswerSubmit,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    test = db.query(Test).filter(Test.id == test_id).first()
    if not test:
        raise HTTPException(status_code=404, detail="Тест не найден")
    
    is_correct = answer_data.answer.strip().lower() == test.correct_answer.strip().lower()
    
    # Сохраняем результат в историю
    result = UserTestResult(
        user_id=current_user.id,
        test_id=test_id,
        answer=answer_data.answer,
        is_correct=is_correct
    )
    db.add(result)
    
    # Обновляем прогресс курса (упрощённо: +5% за правильный ответ)
    enrollment = db.query(UserCourse).filter(UserCourse.user_id == current_user.id).first()
    if enrollment and is_correct:
        enrollment.progress = min(100.0, enrollment.progress + 5.0)
        
    db.commit()
    
    return TestResultResponse(
        test_id=test_id,
        is_correct=is_correct,
        correct_answer=test.correct_answer if not is_correct else None
    )

# 🔹 НОВОЕ: Личный кабинет: мои курсы
@router.get("/my-courses", response_model=list[MyCourseResponse])
def get_my_courses(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    user_courses = db.query(UserCourse).filter(UserCourse.user_id == current_user.id).all()
    
    result = []
    for uc in user_courses:
        course = db.query(Course).filter(Course.id == uc.course_id).first()
        if course:
            result.append(MyCourseResponse(
                course=CourseStudentResponse.model_validate(course),
                progress=uc.progress
            ))
    return result

@router.get("/test-history", response_model=list[TestResultHistory])
def get_test_history(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Просмотр оценок за пройденные тесты"""
    results = (
        db.query(UserTestResult, Test.question)
        .join(Test, UserTestResult.test_id == Test.id)
        .filter(UserTestResult.user_id == current_user.id)
        .order_by(UserTestResult.created_at.desc())
        .all()
    )
    
    return [
        TestResultHistory(
            test_id=res[0].test_id,
            question=res[1],
            your_answer=res[0].answer,
            is_correct=res[0].is_correct,
            submitted_at=res[0].created_at
        )
        for res in results
    ]
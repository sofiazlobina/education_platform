from fastapi import FastAPI
from app.core.config import get_settings
from app.api.auth import router as auth_router
from app.api.courses import router as courses_router 
from app.api.lessons import router as lessons_router
from app.api.tests import router as tests_router
from app.api.students import router as students_router

# Подтягиваю настройки
settings = get_settings()

# Поднимаю приложение FastAPI
# Важно: переменная должна называться "app", иначе все развалится
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION
)

# Подключаю роутер авторизации
app.include_router(auth_router)
app.include_router(courses_router)
app.include_router(lessons_router)
app.include_router(tests_router)
app.include_router(students_router)

# Простой пинг, чтобы понять что сервер жив
@app.get("/")
async def root():
    return {
        "message": "Welcome to Educational Platform API",
        "version": settings.APP_VERSION
    }

@app.get("/health")
async def health_check():
    return {"status": "ok"}
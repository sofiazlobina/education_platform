### Структура проекта
```
educational_platform/
├── app/
│   ├── api/              # API endpoints (роуты)
│   │   ├── __init__.py
│   │   ├── auth.py       # Аутентификация (регистрация, логин, смена пароля)
│   │   ├── courses.py    # CRUD курсов (админ + студент)
│   │   ├── lessons.py    # CRUD уроков
│   │   ├── students.py   # Студенческий API (запись, тесты, прогресс)
│   │   ├── tests.py      # CRUD тестов
│   │   └── __init__.py
│   │
│   ├── core/             # Ядро приложения
│   │   ├── config.py     # Настройки (из .env)
│   │   ├── database.py   # Подключение к БД, сессии
│   │   ├── deps.py       # Зависимости (get_db, get_current_user)
│   │   └── security.py   # Хеширование паролей, JWT токены
│   │
│   ├── models/           # SQLAlchemy модели (таблицы БД)
│   │   ├── __init__.py
│   │   ├── course.py     # Course, Lesson, Test
│   │   ├── test_result.py # UserTestResult (история тестов)
│   │   ├── user.py       # User
│   │   └── user_course.py # UserCourse (прогресс)
│   │
│   ├── schemas/          # Pydantic схемы (валидация)
│   │   ├── __init__.py
│   │   ├── course.py     # CourseCreate, CourseResponse
│   │   ├── lesson.py     # LessonCreate, LessonResponse
│   │   ├── student.py    # TestAnswerSubmit, TestResultHistory
│   │   ├── test.py       # TestCreate, TestResponse
│   │   └── user.py       # UserCreate, UserResponse, Token
│   │
│   └── main.py           # Точка входа, подключение роутеров
│
├── alembic/              # Миграции БД
│   ├── versions/         # Файлы миграций
│   ├── env.py            # Настройка Alembic
│   └── script.py.mako
│
├── tests/                # Тесты (pytest)
│   ├── test_auth.py      # Тесты аутентификации
│   ├── test_courses.py   # Тесты курсов
│   └── conftest.py       # Фикстуры для тестов
│
├── .env                  # Переменные окружения (НЕ коммитить!)
├── .env.example          # Шаблон переменных (можно коммитить)
├── .gitignore            # Игнорируемые файлы
├── alembic.ini           # Настройки Alembic
├── docker-compose.yml    # Docker Compose конфигурация
├── Dockerfile            # Docker образ
├── requirements.txt      # Python зависимости
├── README.md             # Основная документация
└── DEVELOPMENT.md        # Этот файл
```

###  Где что реализован

####  Файлы:
1. app/api/auth.py - эндпоинты (register, login, change-password, refresh-token)
2. app/core/security.py - функции безопасности:
3. verify_password() - проверка пароля
4. get_password_hash() - хеширование
5. create_access_token() - создание JWT
6. get_current_user() - получение текущего пользователя из токена
7. app/models/user.py - модель User
8. app/schemas/user.py - схемы (UserCreate, UserResponse, Token)

####  Как добавить новую функцию:
1. Добавь эндпоинт в app/api/auth.py
2. При необходимости создай схему в app/schemas/user.py
3. Используй get_current_user для защиты роута

### Админ-панель (CRUD)
####  Курсы
####  Файл: app/api/courses.py
- POST /api/v1/admin/courses - создание
- GET /api/v1/admin/courses - список
- GET /api/v1/admin/courses/{id} - получение
- PUT /api/v1/admin/courses/{id} - обновление
- DELETE /api/v1/admin/courses/{id} - удаление
####  Модель: app/models/course.py (класс Course)
####  Схемы: app/schemas/course.py (CourseCreate, CourseUpdate, CourseResponse)

###  Уроки
####  Файл: app/api/lessons.py
- Все CRUD операции для уроков
####  Модель: app/models/course.py (класс Lesson)
####  Схемы: app/schemas/lesson.py

###  Тесты
####  Файл: app/api/tests.py
- Все CRUD операции для тестов
####  Модель: app/models/course.py (класс Test)
####  Схемы: app/schemas/test.py


###  Студенческий API
####  Файл: app/api/students.py
####  Эндпоинты:
- GET /api/v1/student/courses - каталог курсов
- GET /api/v1/student/courses/{id} - детали курса
- GET /api/v1/student/lessons/{id} - получение урока
- GET /api/v1/student/tests/{id} - получение теста
- POST /api/v1/student/courses/{id}/enroll - запись на курс
- POST /api/v1/student/tests/{id}/submit - отправка ответа (с сохранением в историю)
- GET /api/v1/student/my-courses - мои курсы с прогрессом
- GET /api/v1/student/test-history - история результатов тестов

####  Модели:
- app/models/user_course.py - UserCourse (связь пользователь-курс + прогресс)
- app/models/test_result.py - UserTestResult (история тестов)
####  Схемы: app/schemas/student.py

### База данных

####  Подключение: app/core/database.py
```
engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
```

####  Модели (таблицы):
- app/models/user.py -> таблица users
- app/models/course.py -> таблицы courses, lessons, tests
- app/models/user_course.py -> таблица user_courses
- app/models/test_result.py -> таблица user_test_results

####  Миграции:
- Создание: alembic revision --autogenerate -m "description"
- Применение: alembic upgrade head
- Откат: alembic downgrade -1

###  Конфигурация
####  Файл: app/core/config.py

####  Как добавить новую переменную:
- Добавь в .env.example: NEW_VAR=value
- Добавь в app/core/config.py:

```
class Settings(BaseSettings):
    NEW_VAR: str = "default"
```

###  Тестирование

####  Файлы:
- tests/test_auth.py - тесты регистрации, логина
- tests/test_courses.py - тесты курсов
- tests/conftest.py - фикстуры (тестовая БД, клиент)

####  Запуск:
```
pytest tests/ -v                    # Все тесты
pytest tests/test_auth.py -v        # Конкретный файл
pytest tests/ -v --cov=app          # С покрытием
```

####  Как добавить тест:
1. Создай файл tests/test_feature.py
2. Используй фикстуры из conftest.py

```
def test_something(client, test_db):
    response = client.post("/api/v1/auth/login", data={...})
    assert response.status_code == 200
```

### Как добавить новую функцию

#### Пример: Добавить рейтинг курсов
1. Создай модель (app/models/course.py):
```
class CourseRating(Base):
    __tablename__ = "course_ratings"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    course_id = Column(Integer, ForeignKey("courses.id"))
    rating = Column(Integer)  # 1-5
```

2. Создай схему (app/schemas/course.py):
```
class CourseRatingCreate(BaseModel):
    rating: int = Field(..., ge=1, le=5)

class CourseRatingResponse(BaseModel):
    course_id: int
    user_id: int
    rating: int
```

3. Добавь эндпоинт (app/api/courses.py):
```
@router.post("/admin/courses/{course_id}/rate")
def rate_course(
    course_id: int,
    rating_data: CourseRatingCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    rating = CourseRating(
        user_id=current_user.id,
        course_id=course_id,
        rating=rating_data.rating
    )
    db.add(rating)
    db.commit()
    return {"message": "Рейтинг добавлен"}
```

4. Создай миграцию:
```
alembic revision --autogenerate -m "add course ratings"
alembic upgrade head
```

5. Добавь тест (tests/test_ratings.py)

### Полезные команды
```
# Активация venv
.\venv\Scripts\Activate.ps1

# Установка зависимостей
pip install -r requirements.txt

# Запуск сервера
uvicorn app.main:app --reload --port 8001

# Проверка таблиц в БД
python -c "from app.core.database import SessionLocal; from sqlalchemy import inspect; db = SessionLocal(); print(inspect(db.bind).get_table_names())"

# Создание суперпользователя
python make_admin.py

# Просмотр текущей миграции
alembic current

# Откат последней миграции
alembic downgrade -1
```
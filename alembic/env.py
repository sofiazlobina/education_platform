from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context
import sys
import os

# ВАЖНО: Добавляем корень проекта в пути Python, 
# чтобы Alembic мог импортировать модуль 'app'
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Импортируем Base, от которого наследуются все модели
from app.core.database import Base

# Импортируем сами модели, чтобы они "зарегистрировались" в Base.metadata
# Без этого Alembic не увидит таблицы!
from app.models import user
from app.models import course
from app.models import lesson
from app.models import test
from app.models import user_course

# this is the Alembic Config object
config = context.config

import os
# Если в Docker передана переменная DATABASE_URL, используем её (PostgreSQL)
db_url = os.getenv("DATABASE_URL")
if db_url:
    config.set_main_option("sqlalchemy.url", db_url)
# Если переменной нет, будет использована та, что в alembic.ini (SQLite)

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Подключаем метаданные наших моделей
target_metadata = Base.metadata

def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
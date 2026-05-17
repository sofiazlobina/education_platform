from sqlalchemy import create_engine, text

# Подключаюсь к базе, надеюсь она проснулась
engine = create_engine("sqlite:///./educational_platform.db")

print("📋 Список таблиц в базе данных:")

try:
    with engine.connect() as conn:
        # Лезу в служебную таблицу SQLite, тут лежит список таблиц
        result = conn.execute(text("SELECT name FROM sqlite_master WHERE type='table';"))
        tables = result.fetchall()
        
        if not tables:
            print("⚠️ Таблиц не найдено.")
        else:
            for table in tables:
                print(f"✅ {table[0]}")
except Exception as e:
    print(f"❌ Ошибка: {e}")
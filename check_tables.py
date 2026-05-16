from sqlalchemy import create_engine, text

# Подключаемся к нашей базе
engine = create_engine("sqlite:///./educational_platform.db")

print("📋 Список таблиц в базе данных:")

try:
    with engine.connect() as conn:
        # Запрос к системной таблице SQLite, где хранится список всех таблиц
        result = conn.execute(text("SELECT name FROM sqlite_master WHERE type='table';"))
        tables = result.fetchall()
        
        if not tables:
            print("⚠️ Таблиц не найдено.")
        else:
            for table in tables:
                print(f"✅ {table[0]}")
except Exception as e:
    print(f"❌ Ошибка: {e}")
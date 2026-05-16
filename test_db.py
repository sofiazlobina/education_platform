from app.core.database import engine

print("🔍 Проверяем подключение к базе данных...")
try:
    with engine.connect() as conn:
        print("✅ Успешно! База данных подключена.")
except Exception as e:
    print(f"❌ Ошибка подключения: {e}")
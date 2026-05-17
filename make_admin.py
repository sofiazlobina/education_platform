from app.core.database import SessionLocal
from app.models.user import User

def promote_to_admin():
    db = SessionLocal()
    try:
        # Ищу пользователя student1
        user = db.query(User).filter(User.username == "student1").first()
        
        if user:
            user.is_superuser = True  # Делаю админом, пусть будет
            db.commit()
            print(f"✅ Успешно! Пользователь {user.username} теперь АДМИНИСТРАТОР!")
        else:
            print("❌ Пользователь student1 не найден. Сначала зарегистрируйся через API.")
    finally:
        db.close()

if __name__ == "__main__":
    promote_to_admin()
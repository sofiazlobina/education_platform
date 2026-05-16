from fastapi import APIRouter, Depends, HTTPException, status, Body
from sqlalchemy.orm import Session
from app.core.deps import get_db, get_current_user
from app.core.security import get_password_hash, verify_password, create_access_token
from app.models.user import User
from app.schemas.user import UserCreate, UserLogin, UserResponse
from datetime import timedelta
from app.core.config import get_settings
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(prefix="/api/v1/auth", tags=["Auth"])
settings = get_settings()

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    # 1. Проверяем, нет ли уже такого логина
    existing_user = db.query(User).filter(User.username == user_data.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Пользователь с таким логином уже существует")

    # 2. Хэшируем пароль и создаём запись в БД
    hashed_pw = get_password_hash(user_data.password)
    new_user = User(
        username=user_data.username,
        hashed_password=hashed_pw,
        first_name=user_data.first_name,
        last_name=user_data.last_name
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),  # Принимаем форму
    db: Session = Depends(get_db)
):
    # 1. Ищем пользователя
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Неверный логин или пароль")

    # 2. Генерируем токен
    access_token = create_access_token(
        data={"sub": user.username},
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/change-password")
def change_password(
    current_password: str = Body(..., embed=True),
    new_password: str = Body(..., embed=True),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Смена пароля авторизованным пользователем"""
    if not verify_password(current_password, current_user.hashed_password):
        raise HTTPException(status_code=400, detail="Неверный текущий пароль")
    
    current_user.hashed_password = get_password_hash(new_password)
    db.commit()
    return {"message": "Пароль успешно изменён"}

@router.post("/refresh-token")
def refresh_token(current_user: User = Depends(get_current_user)):
    """Обновление access-токена"""
    new_token = create_access_token(data={"sub": current_user.username})
    return {"access_token": new_token, "token_type": "bearer"}
from fastapi import Depends, HTTPException, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import jwt
from app.dependencies import get_async_db, get_current_user
from app.schemas.user import UserDB
from app.models.user import UserCreate, UserUpdate, UserResponse
from app.services.user import UserService
from app.core.config import settings

router = APIRouter(tags=["users"], prefix="/users")

@router.post("/register", response_model=UserResponse, status_code=201)
async def register(user: UserCreate, db: Session = Depends(get_async_db)):
    """Регистрация нового пользователя."""
    try:
        return UserService(db).create_user(user)
    except ValueError as e:
        raise HTTPException(status_code=400, detail={"error": str(e)})

@router.post("/auth/login")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_async_db)
):
    """Аутентификация пользователя с выдачей access и refresh токенов."""
    user = UserService(db).authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=401,
            detail={"error": "Incorrect phone or password"},
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE)
    refresh_token_expires = timedelta(days=7)
    access_token = jwt.encode(
        {"sub": str(user.id), "exp": datetime.utcnow() + access_token_expires},
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )
    refresh_token = jwt.encode(
        {"sub": str(user.id), "exp": datetime.utcnow() + refresh_token_expires},
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }

@router.post("/auth/refresh")
async def refresh_token(refresh_token: str, db: Session = Depends(get_async_db)):
    """Обновление access токена по refresh токену."""
    try:
        payload = jwt.decode(refresh_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id = payload.get("sub")
        user = UserService(db).get_user_by_id(user_id)
        if not user:
            raise HTTPException(status_code=401, detail="Invalid refresh token")
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE)
        access_token = jwt.encode(
            {"sub": str(user.id), "exp": datetime.utcnow() + access_token_expires},
            settings.SECRET_KEY,
            algorithm=settings.ALGORITHM
        )
        return {"access_token": access_token, "token_type": "bearer"}
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Refresh token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

@router.put("/me", response_model=UserResponse)
async def update_user(
    update_data: UserUpdate,
    current_user: UserDB = Depends(get_current_user),
    db: Session = Depends(get_async_db)
):
    """Обновление данных текущего пользователя."""
    try:
        return UserService(db).update_user(current_user.id, update_data)
    except ValueError as e:
        raise HTTPException(status_code=404, detail={"error": str(e)})

@router.delete("/me")
async def delete_user(
    current_user: UserDB = Depends(get_current_user),
    db: Session = Depends(get_async_db)
):
    """Удаление текущего пользователя."""
    if not UserService(db).delete_user(current_user.id):
        raise HTTPException(status_code=404, detail={"error": "User not found"})
    return {"message": "User deactivated"}
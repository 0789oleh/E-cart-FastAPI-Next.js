from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends
from app.db.session import AsyncSessionLocal
from app.core.config import settings
from app.models.user import UserResponse
from app.services.user import UserService


# # Синхронная сессия (для стандартных эндпоинтов)
# def get_db() -> Session:
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

# Асинхронная сессия (для async эндпоинтов)
async def get_async_db() -> AsyncSession:
    async with AsyncSessionLocal() as db:
        yield db


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_async_db)
) -> UserResponse:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        # 1. Декодируем JWT
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,  # Секретный ключ из настроек
            algorithms=[settings.ALGORITHM]  # Обычно "HS256"
        )
        user_id = int(payload.get("sub"))
        if user_id is None:
            raise credentials_exception
    except (JWTError, ValueError):
        raise credentials_exception
    
    # 2. Ищем пользователя в БД
    user = await UserService(db).get_user_by_id(user_id)
    if user is None or not user.is_active:
        raise credentials_exception
    
    return user
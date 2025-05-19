from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt
from datetime import datetime, timedelta
import os
from sqlalchemy.orm import Session
from app.models.user import UserCreate, UserLogin, UserUpdate, UserResponse
from app.services.user import UserService
from app.dependencies import get_async_db, get_current_user
from app.schemas.user import UserDB


router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

# Конфиг JWT
SECRET_KEY = os.getenv("JWT_SECRET")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE = 30  # минуты

@router.post("/register", response_model=UserResponse)
async def register(user: UserCreate, db: Session = Depends(get_async_db)):
    try:
        db_user = UserService(db).create_user(user)
        return db_user
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/auth/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_async_db)):
    user = UserService(db).authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect phone or password",
        )
    
    # JWT generation
    expires = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE)
    token_data = {"sub": str(user.id), "exp": expires}
    token = jwt.encode(token_data, SECRET_KEY, algorithm=ALGORITHM)
    
    return {"access_token": token, "token_type": "bearer"}

@router.put("/me", response_model=UserResponse)
async def update_user(
    update_data: UserUpdate,
    current_user: UserDB = Depends(get_current_user),
    db: Session = Depends(get_async_db)
):
    try:
        return UserService(db).update_user(current_user.id, update_data)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.delete("/me")
async def delete_user(
    current_user: UserDB = Depends(get_current_user),
    db: Session = Depends(get_async_db)
):
    if not UserService(db).delete_user(current_user.id):
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deactivated"}
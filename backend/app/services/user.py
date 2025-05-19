from sqlalchemy.orm import Session
from app.schemas.user import UserDB
from app.models.user import UserCreate, UserUpdate, UserResponse
from typing import Optional

class UserService:
    def __init__(self, db: Session):
        self.db = db

    def create_user(self, user: UserCreate) -> UserDB:
        # Проверка на существующий номер
        if self.db.query(UserDB).filter(UserDB.phone_number == user.phone_number).first():
            raise ValueError("User with this phone already exists")
        
        db_user = UserDB(
            full_name=user.full_name,
            phone_number=user.phone_number
        )
        db_user.set_password(user.password)
        self.db.add(db_user)
        self.db.commit()
        return db_user

    def authenticate_user(self, phone: str, password: str) -> Optional[UserDB]:
        user = self.db.query(UserDB).filter(UserDB.phone_number == phone).first()
        if not user or not user.verify_password(password):
            return None
        return user

    def update_user(self, user_id: int, update_data: UserUpdate) -> UserDB:
        user = self.db.query(UserDB).filter(UserDB.id == user_id).first()
        if not user:
            raise ValueError("User not found")
        
        if update_data.full_name:
            user.full_name = update_data.full_name
        if update_data.password:
            user.set_password(update_data.password)
        
        self.db.commit()
        return user

    def delete_user(self, user_id: int) -> bool:
        user = self.db.query(UserDB).filter(UserDB.id == user_id).first()
        if not user:
            return False
        
        user.is_active = False  # Мягкое удаление
        self.db.commit()
        return True

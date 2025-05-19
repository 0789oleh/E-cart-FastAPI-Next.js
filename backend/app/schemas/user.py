from sqlalchemy import Column, ForeignKey, Integer, Float, String, Boolean
from sqlalchemy.dialects.postgresql import UUID
from app.db.base import Base
import uuid

class UserDB(Base):
    __tablename__ = "users"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    full_name = Column(String(100), nullable=False)
    password = Column(String(25), nullable = False)
    phone_number = Column(String(17), nullable=False)
    is_active = Column(Boolean, default=True)

    def set_password(self, password: str):
        self.password_hash = pwd_context.hash(password)

    def verify_password(self, password: str) -> bool:
        return pwd_context.verify(password, self.password_hash)

from pydantic import BaseModel, Field, EmailStr, field_validator
from typing import Optional
import re

class UserBase(BaseModel):
    full_name: str = Field(..., min_length=2, max_length=100)
    phone_number: str = Field(..., pattern=r"^\+[0-9]{10,15}$")  # E.164

class UserCreate(UserBase):
    password: str = Field(..., min_length=8)
    
    @field_validator('password')
    def validate_password(cls, v):
        if not re.search(r"[A-Z]", v):
            raise ValueError("Password must contain at least one uppercase letter")
        if not re.search(r"[0-9]", v):
            raise ValueError("Password must contain at least one digit")
        return v

class UserLogin(BaseModel):
    phone_number: str
    password: str

class UserUpdate(BaseModel):
    full_name: Optional[str] = Field(None, min_length=2, max_length=100)
    password: Optional[str] = Field(None, min_length=8)

class UserResponse(UserBase):
    id: int
    is_active: bool

    class Config:
        from_attributes = True
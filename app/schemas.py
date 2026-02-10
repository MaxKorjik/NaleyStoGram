from pydantic import BaseModel, EmailStr
from typing import Optional
from .models import PyObjectId

class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    username : str
    email: EmailStr
    password: str

class UserInDB(UserBase):
    id: PyObjectId
    hashed_password: str

class UserOut(UserBase):
    id: str
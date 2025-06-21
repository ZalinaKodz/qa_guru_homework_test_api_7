from typing import Optional
from pydantic import EmailStr
from sqlmodel import Field, SQLModel

class UserBase(SQLModel):
    email: EmailStr
    first_name: str
    last_name: str
    avatar: Optional[str] = None

class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

class UserCreate(UserBase):
    pass

class UserUpdate(SQLModel):
    email: Optional[EmailStr] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    avatar: Optional[str] = None

class UserResponse(UserBase):
    id: int

    class Config:
        orm_mode = True
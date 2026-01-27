from pydantic import BaseModel, EmailStr
from typing import Optional
from models.enums.Tessitura import Tessitura

class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    tessitura: Optional[Tessitura] = None

    class Config:
        from_attributes = True
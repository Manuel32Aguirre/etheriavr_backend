from pydantic import BaseModel, EmailStr, Field

class UserLoginRequest(BaseModel):
    email: EmailStr = Field(..., example="usuario@dominio.com")
    password: str = Field(..., min_length=8, example="Password123")
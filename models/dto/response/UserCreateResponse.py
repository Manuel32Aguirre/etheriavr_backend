from pydantic import BaseModel, EmailStr
from typing import Optional
from models.enums.Tessitura import Tessitura
from models.dto.response.UserConfigurationResponse import UserConfigurationResponse

class UserCreateResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    tessitura: Optional[Tessitura] = None
    configuration: Optional[UserConfigurationResponse] = None

    class Config:
        from_attributes = True
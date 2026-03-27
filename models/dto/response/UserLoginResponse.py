from pydantic import BaseModel
from typing import Optional
from models.dto.response.UserConfigurationResponse import UserConfigurationResponse

class UserLoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    
    id: int
    username: str
    email: str
    tessitura: Optional[str] = None
    configuration: Optional[UserConfigurationResponse] = None
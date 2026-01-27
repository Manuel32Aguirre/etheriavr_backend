from pydantic import BaseModel, EmailStr, Field, model_validator, field_validator

class UserCreateRequest(BaseModel):
    username: str = Field(..., min_length=5, max_length=20, example="usuario123")
    email: EmailStr = Field(..., example="usuario@dominio.com")
    password: str = Field(..., min_length=8, example="Password123")
    confirm_password: str = Field(..., min_length=8, example="Password123")
    
    @field_validator('username')
    @classmethod
    def username_alphabetical(cls, v: str):
        if not v.isalnum():
            raise ValueError('El nombre de usuario solo puede contener letras y números')
        return v

    @field_validator('password')
    @classmethod
    def password_complexity(cls, v: str):
        if not any(char.isdigit() for char in v):
            raise ValueError('La contraseña debe tener al menos un número')
        return v

    @model_validator(mode='after')
    def check_passwords_match(self) -> 'UserCreateRequest':
        if self.password != self.confirm_password:
            raise ValueError('Las contraseñas no coinciden')
        return self
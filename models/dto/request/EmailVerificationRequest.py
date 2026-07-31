from pydantic import BaseModel, EmailStr, Field


class EmailVerificationRequest(BaseModel):
    email: EmailStr
    token: str = Field(..., min_length=20, max_length=200)


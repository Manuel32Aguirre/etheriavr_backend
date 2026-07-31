from pydantic import BaseModel, EmailStr, Field


class EmailVerificationRequest(BaseModel):
    email: EmailStr
    code: str = Field(..., pattern=r"^\d{6}$")

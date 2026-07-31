from pydantic import BaseModel, EmailStr


class ResendEmailVerificationRequest(BaseModel):
    email: EmailStr

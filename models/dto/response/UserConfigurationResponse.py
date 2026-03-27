from typing import Optional
from pydantic import BaseModel


class UserConfigurationResponse(BaseModel):
    user_id: int
    midi_device_name: Optional[str] = None
    audience_intensity: str

    class Config:
        from_attributes = True
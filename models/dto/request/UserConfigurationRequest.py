from typing import Optional
from pydantic import BaseModel, Field
from models.enums.AudienceIntensity import AudienceIntensity


class UserConfigurationRequest(BaseModel):
    midi_device_name: Optional[str] = Field(default=None, max_length=255, example="Yamaha P-125")
    audience_intensity: Optional[AudienceIntensity] = Field(default=None, example="Medio")
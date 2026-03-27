from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field
from models.enums.Mode import Mode


class PracticeSessionCreateRequest(BaseModel):
    user_id: int = Field(..., gt=0, example=1)
    song_id: int = Field(..., gt=0, example=2)
    practice_datetime: Optional[datetime] = Field(default=None, example="2026-03-27T21:10:00")
    practice_mode: Mode = Field(..., example="PIANO")
    rhythm_score: float = Field(..., example=92.4)
    harmony_score: Optional[float] = Field(default=None, example=88.1)
    tuning_score: Optional[float] = Field(default=None, example=90.0)
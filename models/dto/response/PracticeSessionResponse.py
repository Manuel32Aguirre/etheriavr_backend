from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class PracticeSessionResponse(BaseModel):
    id: int
    user_id: int
    song_id: int
    practice_datetime: datetime
    practice_mode: str
    rhythm_score: float
    harmony_score: Optional[float] = None
    tuning_score: Optional[float] = None

    class Config:
        from_attributes = True
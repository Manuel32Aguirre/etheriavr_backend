from pydantic import BaseModel
from models.enums.Mode import Mode

class SongResponse(BaseModel):
    id: int
    musical_genre: str
    musical_key: str
    title: str
    duration: int
    mode: str
    tempo: int
    file_path: str
    artist_name: str

    class Config:
        from_attributes = True
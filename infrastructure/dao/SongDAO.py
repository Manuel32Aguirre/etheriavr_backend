from sqlalchemy.orm import Session, joinedload
from models.entities.Song import Song

class SongDAO:
    def __init__(self, db: Session):
        self.db = db

    def getAll(self) -> list[Song]:
        return self.db.query(Song).options(joinedload(Song.artist)).all()

    def getById(self, song_id: int) -> Song:
        return self.db.query(Song).options(joinedload(Song.artist)).filter(Song.id == song_id).first()

    def getByMode(self, mode: str) -> list[Song]:
        return self.db.query(Song).options(joinedload(Song.artist)).filter(Song.mode == mode).all()
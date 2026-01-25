from domain.repositories.ISongRepository import ISongRepository
from infrastructure.database.models.song_entity import SongEntity
from sqlalchemy.orm import Session
from domain.entities.song import Song

class SongRepositorySQLAlchemy(ISongRepository):
    def __init(self, db: Session):
        self.db = db

    def get_all_songs(self) -> list[Song]:
        song_entities = self.db.query(SongEntity).all()
        return [
            Song(
                song_id=entity.song_id,
                artist_id=entity.artist_id,
                title=entity.title,
                musical_genre=entity.musical_genre,
                musical_key=entity.musical_key,
                original_tempo=entity.original_tempo,
                duration=entity.duration,
                file_path=entity.file_path,
            )
            for entity in song_entities
        ]

    
    def get_song_by_id(self, song_id: int) -> Song | None:
        entity = self.db.query(SongEntity).filter_by(song_id=song_id).first()
        if not entity:
            return None

        return Song(
            song_id=entity.song_id,
            artist_id=entity.artist_id,
            title=entity.title,
            musical_genre=entity.musical_genre,
            musical_key=entity.musical_key,
            original_tempo=entity.original_tempo,
            duration=entity.duration,
            file_path=entity.file_path,
        )
    
    
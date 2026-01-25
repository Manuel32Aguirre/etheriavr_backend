from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from infrastructure.database.connection import Base

class SongEntity(Base):
    __tablename__ = "song"

    song_id = Column(Integer, primary_key=True, autoincrement=True)
    artist_id = Column(Integer, ForeignKey("artist.artist_id"), nullable=False)
    title = Column(String(255), nullable=False)
    musical_genre = Column(String(100))
    musical_key = Column(String(20))
    original_tempo = Column(Integer)
    duration = Column(Integer)
    file_path = Column(String(255))

    # Relaciones
    artist = relationship("ArtistEntity", back_populates="songs")
    practice_sessions = relationship("PracticeSessionEntity", back_populates="song")
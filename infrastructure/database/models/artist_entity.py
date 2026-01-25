from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from infrastructure.database.connection import Base

class ArtistEntity(Base):
    __tablename__ = "artist"

    artist_id = Column(Integer, primary_key=True, autoincrement=True)
    artist_name = Column(String(255), nullable=False)

    # Relaciones
    songs = relationship("SongEntity", back_populates="artist")

from sqlalchemy import Column, Integer, String, ForeignKey, Enum as SQLEnum # Importamos SQLEnum
from sqlalchemy.orm import relationship
from config.connection import Base
from models.enums.Mode import Mode # Importamos tu Enum de Python

class Song(Base):
    __tablename__ = 'songs'

    id = Column(Integer, primary_key=True)
    musical_genre = Column(String(100), nullable=False)
    musical_key = Column(String(10), nullable=False)
    title = Column(String(255), nullable=False)
    duration = Column(Integer, nullable=False)
    mode = Column(SQLEnum(Mode), nullable=False)
    tempo = Column(Integer, nullable=False)    
    file_path = Column(String(500), nullable=False)
    
    artist_id = Column(Integer, ForeignKey("artists.id"), nullable=False)
    artist = relationship("Artist", back_populates="songs")
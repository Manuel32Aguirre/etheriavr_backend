from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from config.connection import Base

class Artist(Base):
    __tablename__ = "artists"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)

    songs = relationship("Song", back_populates="artist")
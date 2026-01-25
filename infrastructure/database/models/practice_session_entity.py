from sqlalchemy import Column, Integer, ForeignKey, DateTime, Enum, Numeric
from sqlalchemy.orm import relationship
from infrastructure.database.connection import Base
import enum

class PracticeMode(str, enum.Enum):
    piano = "piano"
    canto = "canto"

class PracticeSessionEntity(Base):
    __tablename__ = "practice_session"

    session_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("user.user_id"), nullable=False)
    song_id = Column(Integer, ForeignKey("song.song_id"), nullable=False)
    practice_datetime = Column(DateTime)
    practice_mode = Column(Enum(PracticeMode), nullable=False)
    rhythm_score = Column(Numeric(5, 2), nullable=False)
    harmony_score = Column(Numeric(5, 2))
    tuning_score = Column(Numeric(5, 2))

    # Relaciones
    user = relationship("UserEntity", back_populates="practice_sessions")
    song = relationship("SongEntity", back_populates="practice_sessions")

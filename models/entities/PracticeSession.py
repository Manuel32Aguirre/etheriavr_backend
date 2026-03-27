from datetime import datetime
from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, Enum as SQLEnum
from sqlalchemy.orm import relationship
from config.connection import Base
from models.enums.Mode import Mode


class PracticeSession(Base):
    __tablename__ = "practice_sessions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    song_id = Column(Integer, ForeignKey("songs.id"), nullable=False)
    practice_datetime = Column(DateTime, nullable=False, default=datetime.utcnow)
    practice_mode = Column(SQLEnum(Mode), nullable=False)
    rhythm_score = Column(Float, nullable=False)
    harmony_score = Column(Float, nullable=True)
    tuning_score = Column(Float, nullable=True)

    user = relationship("User", back_populates="practice_sessions")
    song = relationship("Song", back_populates="practice_sessions")
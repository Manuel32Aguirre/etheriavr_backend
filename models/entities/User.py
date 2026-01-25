from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from config.connection import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)

    username = Column(String(50), nullable=False, unique=True)
    
    email = Column(String(100), nullable=False, unique=True)
    
    password_hash = Column(String(255), nullable=False)
    
    tessitura = Column(String(50), nullable=True) # Soprano, Tenor, etc.

    practice_sessions = relationship("PracticeSession", back_populates="user")
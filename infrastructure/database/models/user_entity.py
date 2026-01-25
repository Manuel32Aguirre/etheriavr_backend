from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from infrastructure.database.connection import Base

class UserEntity(Base):
    __tablename__ = "user"
    
    user_id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    password_hash = Column(String(255), nullable=False)

    #Relaciones
    practice_sessions = relationship("PracticeSessionEntity", back_populates="user")
    configuration = relationship("UserConfigurationEntity", uselist=False, back_populates="user")
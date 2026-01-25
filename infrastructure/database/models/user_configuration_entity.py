from sqlalchemy import Column, Integer, String, Enum, ForeignKey
from sqlalchemy.orm import relationship
from infrastructure.database.connection import Base
import enum

class AudienceIntensity(str, enum.Enum):
    Bajo = "Bajo"
    Medio = "Medio"
    Alto = "Alto"

class UserConfigurationEntity(Base):
    __tablename__ = "user_configuration"

    user_id = Column(Integer, ForeignKey("user.user_id"), primary_key=True)
    midi_device_name = Column(String(255))
    audience_intensity = Column(Enum(AudienceIntensity), nullable=False)

    # Relaciones
    user = relationship("UserEntity", back_populates="configuration")

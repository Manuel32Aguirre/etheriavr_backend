from sqlalchemy import Column, ForeignKey, Integer, String, Enum as SQLEnum
from sqlalchemy.orm import relationship
from config.connection import Base
from models.enums.AudienceIntensity import AudienceIntensity


class UserConfiguration(Base):
    __tablename__ = "user_configurations"

    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    midi_device_name = Column(String(255), nullable=True)
    audience_intensity = Column(
        SQLEnum(AudienceIntensity),
        nullable=False,
        default=AudienceIntensity.MEDIO
    )

    user = relationship("User", back_populates="user_configuration")
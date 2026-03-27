from sqlalchemy.orm import Session
from models.entities.UserConfiguration import UserConfiguration


class UserConfigurationDAO:
    def __init__(self, db: Session):
        self.db = db

    def save(self, configuration: UserConfiguration) -> UserConfiguration:
        self.db.add(configuration)
        self.db.commit()
        self.db.refresh(configuration)
        return configuration

    def getByUserId(self, user_id: int) -> UserConfiguration:
        return self.db.query(UserConfiguration).filter(UserConfiguration.user_id == user_id).first()
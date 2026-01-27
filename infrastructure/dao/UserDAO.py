from sqlalchemy.orm import Session
from models.entities.User import User

class UserDAO:
    def __init__(self, db: Session):
        self.db = db

    def save(self, user: User) -> User:
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def getByEmail(self, email: str) -> User:
        return self.db.query(User).filter(User.email == email).first()

    def getById(self, user_id: int) -> User:
        return self.db.query(User).filter(User.id == user_id).first()
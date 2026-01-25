from sqlalchemy.orm import Session
from domain.repositories.IUserRepository import IUserRepository
from domain.entities.user import User
from infrastructure.database.models.user_entity import UserEntity


class UserRepositorySQLAlchemy(IUserRepository):
    def __init__(self, db: Session):
        self.db = db

    def register_user(self, user: User) -> User:
        user_entity = UserEntity(
            username=user.username,
            email=user.email,
            password_hash=user.password_hash
        )
        self.db.add(user_entity)
        self.db.commit()
        self.db.refresh(user_entity)

        return User(
            user_id=user_entity.user_id,
            username=user_entity.username,
            email=user_entity.email,
            password_hash=user_entity.password_hash
        )

    def get_user_by_email(self, email: str) -> User | None:
        user_entity = self.db.query(UserEntity).filter_by(email=email).first()
        if not user_entity:
            return None

        return User(
            user_id=user_entity.user_id,
            username=user_entity.username,
            email=user_entity.email,
            password_hash=user_entity.password_hash
        )

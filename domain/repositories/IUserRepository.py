from abc import ABC, abstractmethod

from domain.entities.user import User

class IUserRepository(ABC):

    @abstractmethod
    def register_user(self, user: User) -> User:
        pass

    @abstractmethod
    def get_user_by_email(self, email: str) -> User:
        pass

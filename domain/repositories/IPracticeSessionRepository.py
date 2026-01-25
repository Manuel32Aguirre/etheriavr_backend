from abc import ABC, abstractmethod
from domain.entities.practice_session import PracticeSession

class IPracticeSessionRepository(ABC):

    @abstractmethod
    def save_practice_session(self, session: PracticeSession) -> PracticeSession:
        pass

    @abstractmethod
    def get_all_practice_sessions(self) -> list[PracticeSession]:
        pass

    @abstractmethod
    def get_practice_sessions_by_user_id(self, user_id: int) -> list[PracticeSession]:
        pass


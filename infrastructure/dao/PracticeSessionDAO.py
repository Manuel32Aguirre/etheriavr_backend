from sqlalchemy.orm import Session
from models.entities.PracticeSession import PracticeSession


class PracticeSessionDAO:
    def __init__(self, db: Session):
        self.db = db

    def save(self, session: PracticeSession) -> PracticeSession:
        self.db.add(session)
        self.db.commit()
        self.db.refresh(session)
        return session
from sqlalchemy.orm import Session, joinedload
from models.entities.PracticeSession import PracticeSession


class PracticeSessionDAO:
    def __init__(self, db: Session):
        self.db = db

    def save(self, session: PracticeSession) -> PracticeSession:
        self.db.add(session)
        self.db.commit()
        self.db.refresh(session)
        # Eager-load la relación song para que esté disponible en el mapper
        self.db.expunge(session)
        session = self.db.query(PracticeSession).options(joinedload(PracticeSession.song)).filter_by(id=session.id).first()
        return session
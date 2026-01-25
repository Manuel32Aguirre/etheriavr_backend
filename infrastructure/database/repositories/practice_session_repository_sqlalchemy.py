from domain.entities.practice_session import PracticeSession
from domain.repositories.IPracticeSessionRepository import IPracticeSessionRepository
from sqlalchemy.orm import Session
from infrastructure.database.models.practice_session_entity import PracticeSessionEntity

class PracticeSessionRepositorySQLAlchemy(IPracticeSessionRepository):

    def __init__(self, db: Session):
        self.db = db
    
    
    def save_practice_session(self, session: PracticeSession) -> PracticeSession:
        practice_session_entity = PracticeSessionEntity(
            user_id = session.user_id,
            song_id = session.song_id,
            practice_datetime = session.practice_datetime,
            practice_mode = session.practice_mode,
            rhythm_score = session.rhythm_score,
            harmony_score = session.harmony_score,
            tuning_score = session.tuning_score
        )
        self.db.add(practice_session_entity)
        self.db.commit()
        self.db.refresh(practice_session_entity)

        return PracticeSession(
            session_id = practice_session_entity.session_id,
            user_id = practice_session_entity.user_id,
            song_id = practice_session_entity.song_id,
            practice_datetime = practice_session_entity.practice_datetime,
            practice_mode = practice_session_entity.practice_mode,
            rhythm_score = practice_session_entity.rhythm_score,
            harmony_score = practice_session_entity.harmony_score,
            tuning_score = practice_session_entity.tuning_score
        )

    
    def get_all_practice_sessions(self) -> list[PracticeSession]:
        practice_sessions_entities = self.db.query(PracticeSessionEntity).all()
        return [
            PracticeSession(
                session_id = entity.session_id,
                user_id = entity.user_id,
                song_id = entity.song_id,
                practice_datetime = entity.practice_datetime,
                practice_mode = entity.practice_mode,
                rhythm_score = entity.rhythm_score,
                harmony_score = entity.harmony_score,
                tuning_score = entity.tuning_score
            )
            for entity in practice_sessions_entities
        ]

    
    def get_practice_sessions_by_user_id(self, user_id: int) -> list[PracticeSession]:
        entity = self.db.query(PracticeSessionEntity).filter_by(user_id=user_id).all()
        return [
            PracticeSession(
                session_id = entity.session_id,
                user_id = entity.user_id,
                song_id = entity.song_id,
                practice_datetime = entity.practice_datetime,
                practice_mode = entity.practice_mode,
                rhythm_score = entity.rhythm_score,
                harmony_score = entity.harmony_score,
                tuning_score = entity.tuning_score
            )
            for entity in entity
        ]

    
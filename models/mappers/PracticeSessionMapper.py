from datetime import datetime
from models.dto.request.PracticeSessionCreateRequest import PracticeSessionCreateRequest
from models.dto.response.PracticeSessionResponse import PracticeSessionResponse
from models.entities.PracticeSession import PracticeSession


class PracticeSessionMapper:
    @staticmethod
    def toEntity(request: PracticeSessionCreateRequest) -> PracticeSession:
        return PracticeSession(
            user_id=request.user_id,
            song_id=request.song_id,
            practice_datetime=request.practice_datetime or datetime.utcnow(),
            practice_mode=request.practice_mode,
            rhythm_score=request.rhythm_score,
            harmony_score=request.harmony_score,
            tuning_score=request.tuning_score
        )

    @staticmethod
    def toDto(entity: PracticeSession) -> PracticeSessionResponse:
        return PracticeSessionResponse(
            id=entity.id,
            user_id=entity.user_id,
            song_id=entity.song_id,
            practice_datetime=entity.practice_datetime,
            practice_mode=entity.practice_mode.value,
            rhythm_score=entity.rhythm_score,
            harmony_score=entity.harmony_score,
            tuning_score=entity.tuning_score
        )
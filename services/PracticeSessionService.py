from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from infrastructure.dao.PracticeSessionDAO import PracticeSessionDAO
from infrastructure.dao.SongDAO import SongDAO
from infrastructure.dao.UserDAO import UserDAO
from models.dto.request.PracticeSessionCreateRequest import PracticeSessionCreateRequest
from models.dto.response.PracticeSessionResponse import PracticeSessionResponse
from models.mappers.PracticeSessionMapper import PracticeSessionMapper


class PracticeSessionService:
    def __init__(self, db: Session):
        self.practiceSessionDao = PracticeSessionDAO(db)
        self.userDao = UserDAO(db)
        self.songDao = SongDAO(db)
        self.db = db

    def registrarSesionPractica(self, request: PracticeSessionCreateRequest) -> PracticeSessionResponse:
        usuario = self.userDao.getById(request.user_id)
        if not usuario:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuario no encontrado."
            )

        cancion = self.songDao.getById(request.song_id)
        if not cancion:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Canción no encontrada."
            )

        sesionEntity = PracticeSessionMapper.toEntity(request)
        sesionGuardada = self.practiceSessionDao.save(sesionEntity)
        return PracticeSessionMapper.toDto(sesionGuardada)
    

    # En PracticeSessionService.py
    def obtenerSesionesPorUsuario(self, user_id: int):
        from models.entities.PracticeSession import PracticeSession
        from models.entities.Song import Song

        results = self.db.query(PracticeSession, Song.title).\
            join(Song, PracticeSession.song_id == Song.id).\
            filter(PracticeSession.user_id == user_id).all()
        
        sesiones = []
        for practice, song_title in results:
            # Calcular global_score manejando valores None
            rhythm = practice.rhythm_score or 0
            tuning = practice.tuning_score or 0
            global_score = (rhythm + tuning) / 2 if (practice.rhythm_score is not None or practice.tuning_score is not None) else None
            
            sesiones.append({
                "id": practice.id,
                "user_id": practice.user_id,
                "song_id": practice.song_id,
                "song_title": song_title,
                "practice_datetime": practice.practice_datetime.strftime("%Y-%m-%d %H:%M:%S"),
                "practice_mode": practice.practice_mode.value,
                "rhythm_score": practice.rhythm_score,
                "tuning_score": practice.tuning_score,
                "harmony_score": practice.harmony_score,
                "global_score": global_score
            })
        
        return sesiones
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
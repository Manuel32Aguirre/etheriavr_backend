from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from config.connection import obtenerBD
from models.dto.request.PracticeSessionCreateRequest import PracticeSessionCreateRequest
from models.dto.response.PracticeSessionResponse import PracticeSessionResponse
from services.PracticeSessionService import PracticeSessionService


router = APIRouter(prefix="/api/practice-sessions", tags=["Practice Sessions"])


@router.post("", response_model=PracticeSessionResponse, status_code=status.HTTP_201_CREATED)
def createPracticeSession(request: PracticeSessionCreateRequest, db: Session = Depends(obtenerBD)):
    sesionServicio = PracticeSessionService(db)
    return sesionServicio.registrarSesionPractica(request)
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from config.connection import obtenerBD
from models.dto.request.PracticeSessionCreateRequest import PracticeSessionCreateRequest
from models.dto.response.PracticeSessionResponse import PracticeSessionResponse
from services.PracticeSessionService import PracticeSessionService
from typing import List
from core.security import get_current_user
from models.entities.User import User

router = APIRouter(prefix="/api/practice-sessions", tags=["Practice Sessions"])


@router.post("", response_model=PracticeSessionResponse, status_code=status.HTTP_201_CREATED)
def createPracticeSession(
    request: PracticeSessionCreateRequest,
    db: Session = Depends(obtenerBD),
    current_user: User = Depends(get_current_user),
):
    sesionServicio = PracticeSessionService(db)
    return sesionServicio.registrarSesionPractica(request)



@router.get("/user/{user_id}", response_model=List[PracticeSessionResponse])
def getPracticeSessionsByUser(
    user_id: int,
    db: Session = Depends(obtenerBD),
    current_user: User = Depends(get_current_user),
):
    sesionServicio = PracticeSessionService(db)
    return sesionServicio.obtenerSesionesPorUsuario(user_id)
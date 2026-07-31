from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from config.connection import obtenerBD
from services.SongService import SongService
from models.dto.response.SongResponse import SongResponse
from core.security import get_current_user
from models.entities.User import User

router = APIRouter(prefix="/api/songs", tags=["Songs"])

@router.get("/listar", response_model=list[SongResponse])
def getAllSongs(
    db: Session = Depends(obtenerBD),
    current_user: User = Depends(get_current_user),
):
    
    cancionServicio = SongService(db)
    return cancionServicio.getAllSongs()
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from config.connection import obtenerBD
from services.SongService import SongService
from models.dto.response.SongResponse import SongResponse

router = APIRouter(prefix="/api/songs", tags=["Songs"])

@router.get("/listar", response_model=list[SongResponse])
def getAllSongs(db: Session = Depends(obtenerBD)):
    
    cancionServicio = SongService(db)
    return cancionServicio.getAllSongs()
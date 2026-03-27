from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from config.connection import obtenerBD
from models.dto.request.UserConfigurationRequest import UserConfigurationRequest
from models.dto.response.UserConfigurationResponse import UserConfigurationResponse
from services.UserConfigurationService import UserConfigurationService


router = APIRouter(prefix="/api/users", tags=["User Configuration"])


@router.get("/{user_id}/configuration", response_model=UserConfigurationResponse)
def getUserConfiguration(user_id: int, db: Session = Depends(obtenerBD)):
    configuracionServicio = UserConfigurationService(db)
    return configuracionServicio.obtenerConfiguracionUsuario(user_id)


@router.put("/{user_id}/configuration", response_model=UserConfigurationResponse)
def saveUserConfiguration(user_id: int, request: UserConfigurationRequest, db: Session = Depends(obtenerBD)):
    configuracionServicio = UserConfigurationService(db)
    return configuracionServicio.guardarConfiguracionUsuario(user_id, request)
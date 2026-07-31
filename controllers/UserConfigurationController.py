from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from config.connection import obtenerBD
from models.dto.request.UserConfigurationRequest import UserConfigurationRequest
from models.dto.response.UserConfigurationResponse import UserConfigurationResponse
from services.UserConfigurationService import UserConfigurationService
from core.security import get_current_user
from core.authorization import require_owner
from models.entities.User import User


router = APIRouter(prefix="/api/users", tags=["User Configuration"])


@router.get("/{user_id}/configuration", response_model=UserConfigurationResponse)
def getUserConfiguration(
    user_id: int,
    db: Session = Depends(obtenerBD),
    current_user: User = Depends(get_current_user),
):
    # Prevención IDOR: cada usuario solo puede leer su propia configuración.
    require_owner(user_id, current_user, entity_name="configuración")
    configuracionServicio = UserConfigurationService(db)
    return configuracionServicio.obtenerConfiguracionUsuario(current_user.id)


@router.put("/{user_id}/configuration", response_model=UserConfigurationResponse)
def saveUserConfiguration(
    user_id: int,
    request: UserConfigurationRequest,
    db: Session = Depends(obtenerBD),
    current_user: User = Depends(get_current_user),
):
    # Prevención IDOR: cada usuario solo puede modificar su propia configuración.
    require_owner(user_id, current_user, entity_name="configuración")
    configuracionServicio = UserConfigurationService(db)
    return configuracionServicio.guardarConfiguracionUsuario(current_user.id, request)

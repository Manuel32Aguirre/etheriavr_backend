from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from infrastructure.dao.UserConfigurationDAO import UserConfigurationDAO
from infrastructure.dao.UserDAO import UserDAO
from models.dto.request.UserConfigurationRequest import UserConfigurationRequest
from models.dto.response.UserConfigurationResponse import UserConfigurationResponse
from models.mappers.UserConfigurationMapper import UserConfigurationMapper


class UserConfigurationService:
    def __init__(self, db: Session):
        self.userDao = UserDAO(db)
        self.configurationDao = UserConfigurationDAO(db)

    def obtenerConfiguracionUsuario(self, user_id: int) -> UserConfigurationResponse:
        usuario = self.userDao.getById(user_id)
        if not usuario:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuario no encontrado."
            )

        configuracion = self.configurationDao.getByUserId(user_id)
        if not configuracion:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Configuración de usuario no encontrada."
            )

        return UserConfigurationMapper.toDto(configuracion)

    def guardarConfiguracionUsuario(self, user_id: int, request: UserConfigurationRequest) -> UserConfigurationResponse:
        usuario = self.userDao.getById(user_id)
        if not usuario:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuario no encontrado."
            )

        configuracion = self.configurationDao.getByUserId(user_id)

        if not configuracion:
            configuracion = UserConfigurationMapper.toEntityFromRequest(user_id, request)
        else:
            if request.midi_device_name is not None:
                configuracion.midi_device_name = request.midi_device_name
            if request.audience_intensity is not None:
                configuracion.audience_intensity = request.audience_intensity

        configuracionGuardada = self.configurationDao.save(configuracion)
        return UserConfigurationMapper.toDto(configuracionGuardada)
from models.entities.User import User
from models.dto.request.UserCreateRequest import UserCreateRequest
from models.dto.response.UserCreateResponse import UserCreateResponse
from core.security import get_password_hash
from models.dto.response.UserLoginResponse import UserLoginResponse
from models.mappers.UserConfigurationMapper import UserConfigurationMapper

class UserMapper:

    # --- DE REQUEST A ENTIDAD ---
    @staticmethod
    def toEntity(request: UserCreateRequest, password_hash: str) -> User:
        return User(
            username=request.username,
            email=request.email,
            password_hash=password_hash 
            # La tessitura se queda en NULL por defecto en el modelo
        )

    # --- DE ENTIDAD A RESPONSE (REGISTRO) ---
    @staticmethod
    def toDto(entity: User) -> UserCreateResponse:
        """Convierte Entidad de DB a DTO de salida seguro"""
        return UserCreateResponse(
            id=entity.id,
            username=entity.username,
            email=entity.email,
            tessitura=entity.tessitura,
            configuration=UserConfigurationMapper.toDto(entity.user_configuration)
        )
    
# --- DE ENTIDAD A RESPONSE (LOGIN) ---
    @staticmethod
    def toLoginDto(entity: User, token: str) -> UserLoginResponse:
        """Para el inicio de sesión (incluye el JWT)"""
        return UserLoginResponse(
            access_token=token,
            id=entity.id,
            username=entity.username,
            email=entity.email,
            tessitura=entity.tessitura,
            configuration=UserConfigurationMapper.toDto(entity.user_configuration)
        )

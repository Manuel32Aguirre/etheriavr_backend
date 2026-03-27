from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from infrastructure.dao.UserDAO import UserDAO
from models.dto.response.UserCreateResponse import UserCreateResponse
from models.entities.User import User
from models.dto.request.UserCreateRequest import UserCreateRequest
from core.security import get_password_hash
from core.security import verify_password, create_access_token # Asumiendo que tienes estas utilerías
from models.dto.response.UserLoginResponse import UserLoginResponse
from models.dto.request.UserLoginRequest import UserLoginRequest
from models.mappers.UserMapper import UserMapper
from models.mappers.UserConfigurationMapper import UserConfigurationMapper

class UserService:
    def __init__(self, db: Session):
        self.usuarioDao = UserDAO(db)

    def registrarUsuario(self, request: UserCreateRequest) -> UserCreateResponse:
        # 1. Validación de existencia
        if self.usuarioDao.getByEmail(request.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El correo electrónico ya está registrado."
            )
        
        # 2. Hashear y Mapear a Entidad
        pwd_hash = get_password_hash(request.password)
        usuarioEntity = UserMapper.toEntity(request, pwd_hash)
        usuarioEntity.user_configuration = UserConfigurationMapper.toEntity(request)

        # 3. Guardar
        usuarioSaved = self.usuarioDao.save(usuarioEntity)

        # 4. Mapear a Response DTO
        return UserMapper.toDto(usuarioSaved)
    
    def loginUsuario(self, request: UserLoginRequest) -> UserLoginResponse:
        usuarioBuscado = self.usuarioDao.getByEmail(request.email)
        
        # 2. Verificar existencia y contraseña
        if not usuarioBuscado or not verify_password(request.password, usuarioBuscado.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Credenciales incorrectas."
            )

        # 3. Generar el Token (JWT)
        access_token = create_access_token(data={"sub": str(usuarioBuscado.id)})

        # 4. Mapear la SALIDA (Aquí sí es obligatorio el Mapper)
        # Convertimos la Entidad "sucia" (con hash) en un DTO "seguro" con Token
        return UserMapper.toLoginDto(usuarioBuscado, access_token)
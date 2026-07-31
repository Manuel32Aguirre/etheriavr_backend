from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from infrastructure.dao.UserDAO import UserDAO
from models.dto.response.UserCreateResponse import UserCreateResponse
from models.entities.User import User
from models.dto.request.UserCreateRequest import UserCreateRequest
from datetime import datetime, timedelta
import secrets

from core.security import get_password_hash
from core.security import verify_password, create_access_token # Asumiendo que tienes estas utilerías
from models.dto.response.UserLoginResponse import UserLoginResponse
from models.dto.request.UserLoginRequest import UserLoginRequest
from models.mappers.UserMapper import UserMapper
from models.mappers.UserConfigurationMapper import UserConfigurationMapper
from models.dto.request.EmailVerificationRequest import EmailVerificationRequest
from services.EmailService import EmailService

class UserService:
    def __init__(self, db: Session):
        self.usuarioDao = UserDAO(db)

    @staticmethod
    def _generar_codigo_verificacion() -> str:
        return f"{secrets.randbelow(1_000_000):06d}"

    @staticmethod
    def _fecha_expiracion_codigo() -> datetime:
        return datetime.utcnow() + timedelta(
            minutes=EmailService.verification_code_expire_minutes()
        )

    def registrarUsuario(self, request: UserCreateRequest) -> UserCreateResponse:
        # 1. Validación de existencia
        if self.usuarioDao.getByEmail(request.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El correo electrónico ya está registrado."
            )
        
        # 2. Crear un código de un solo uso y almacenar únicamente su hash.
        pwd_hash = get_password_hash(request.password)
        verification_code = self._generar_codigo_verificacion()
        usuarioEntity = UserMapper.toEntity(
            request,
            pwd_hash,
            get_password_hash(verification_code),
            self._fecha_expiracion_codigo(),
        )
        usuarioEntity.user_configuration = UserConfigurationMapper.toEntity(request)

        # 3. Guardar
        usuarioSaved = self.usuarioDao.save(usuarioEntity)

        # 4. Enviar la confirmación después de persistir el usuario.
        EmailService.send_verification_code(usuarioSaved.email, verification_code)

        # 5. Mapear a Response DTO
        return UserMapper.toDto(usuarioSaved)
    
    def loginUsuario(self, request: UserLoginRequest) -> UserLoginResponse:
        usuarioBuscado = self.usuarioDao.getByEmail(request.email)
        
        # 2. Verificar existencia y contraseña
        if not usuarioBuscado or not verify_password(request.password, usuarioBuscado.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Credenciales incorrectas."
            )

        if not usuarioBuscado.email_verified:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Confirma tu correo electrónico antes de iniciar sesión."
            )

        # 3. Generar el Token (JWT)
        access_token = create_access_token(data={"sub": str(usuarioBuscado.id)})

        # 4. Mapear la SALIDA (Aquí sí es obligatorio el Mapper)
        # Convertimos la Entidad "sucia" (con hash) en un DTO "seguro" con Token
        return UserMapper.toLoginDto(usuarioBuscado, access_token)

    def verificarCorreo(self, request: EmailVerificationRequest) -> None:
        usuario = self.usuarioDao.getByEmail(request.email)
        if not usuario or not usuario.email_verification_code_hash:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El código de confirmación no es válido."
            )

        if usuario.email_verified:
            return

        if (
            not usuario.email_verification_expires_at
            or usuario.email_verification_expires_at < datetime.utcnow()
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El código de confirmación ha expirado. Solicita uno nuevo."
            )

        if not verify_password(request.code, usuario.email_verification_code_hash):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El código de confirmación no es válido."
            )

        usuario.email_verified = True
        usuario.email_verification_code_hash = None
        usuario.email_verification_expires_at = None
        self.usuarioDao.save(usuario)

    def reenviarCodigoConfirmacion(self, email: str) -> None:
        usuario = self.usuarioDao.getByEmail(email)
        if not usuario:
            return

        if usuario.email_verified:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El correo electrónico ya fue confirmado."
            )

        verification_code = self._generar_codigo_verificacion()
        usuario.email_verification_code_hash = get_password_hash(verification_code)
        usuario.email_verification_expires_at = self._fecha_expiracion_codigo()
        self.usuarioDao.save(usuario)
        EmailService.send_verification_code(usuario.email, verification_code)
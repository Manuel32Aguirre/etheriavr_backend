from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from infrastructure.dao.UserDAO import UserDAO
from models.entities.User import User
from models.dto.request.UserCreateRequest import UserCreateRequest
from core.security import get_password_hash

class UserService:
    def __init__(self, db: Session):
        self.usuarioDao = UserDAO(db)

    def registrarUsuario(self, request: UserCreateRequest) -> User:
        
        if self.usuarioDao.getByEmail(request.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El correo electrónico ya está registrado."
            )
        
        usuario = User(
            username=request.username,
            email=request.email,
            password_hash=get_password_hash(request.password)
        )

        return self.usuarioDao.save(usuario)
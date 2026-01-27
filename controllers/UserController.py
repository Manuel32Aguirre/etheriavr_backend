from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from config.connection import obtenerBD
from models.dto.request.UserCreateRequest import UserCreateRequest
from models.dto.response.UserResponse import UserResponse
from services.UserService import UserService

router = APIRouter(prefix="/api", tags=["Users"])

@router.post("/users", response_model=UserResponse, status_code=status.HTTP_201_CREATED,summary="Registrar un nuevo usuario",description="Crea un usuario en la base de datos y devuelve su información pública.")
def register(request: UserCreateRequest, db: Session = Depends(obtenerBD)):

    usuarioServicio = UserService(db)

    return usuarioServicio.registrarUsuario(request)
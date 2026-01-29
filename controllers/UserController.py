from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from config.connection import obtenerBD
from models.dto.request.UserCreateRequest import UserCreateRequest
from models.dto.request.UserLoginRequest import UserLoginRequest
from models.dto.response.UserCreateResponse import UserCreateResponse
from models.dto.response.UserLoginResponse import UserLoginResponse
from services.UserService import UserService

router = APIRouter(prefix="/api", tags=["Users"])

@router.post("/users", response_model=UserCreateResponse, status_code=status.HTTP_201_CREATED)
def register(request: UserCreateRequest, db: Session = Depends(obtenerBD)):
    usuarioServicio = UserService(db)
    return usuarioServicio.registrarUsuario(request)

@router.post("/login", response_model=UserLoginResponse)
def login(request: UserLoginRequest, db: Session = Depends(obtenerBD)):
    usuarioServicio = UserService(db)
    return usuarioServicio.loginUsuario(request)
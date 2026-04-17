from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from config.connection import obtenerBD
from models.entities.User import User  # IMPORTANTE: Asegúrate de que esta ruta sea correcta
from models.dto.request.UserCreateRequest import UserCreateRequest
from models.dto.request.UserTessituraRequest import UserTessituraRequest
from models.dto.request.UserLoginRequest import UserLoginRequest
from models.dto.response.UserCreateResponse import UserCreateResponse
from models.dto.response.UserLoginResponse import UserLoginResponse
from services.UserService import UserService

# Usamos un solo router para no causar conflictos de prefijos
router = APIRouter(prefix="/api", tags=["Users"])

@router.post("/users", response_model=UserCreateResponse, status_code=status.HTTP_201_CREATED)
def register(request: UserCreateRequest, db: Session = Depends(obtenerBD)):
    usuarioServicio = UserService(db)
    return usuarioServicio.registrarUsuario(request)

@router.post("/login", response_model=UserLoginResponse)
def login(request: UserLoginRequest, db: Session = Depends(obtenerBD)):
    usuarioServicio = UserService(db)
    return usuarioServicio.loginUsuario(request)

# El endpoint de tessitura bajo el prefijo /api/users
@router.put("/users/{user_id}/tessitura")
async def update_tessitura(user_id: int, request: UserTessituraRequest, db: Session = Depends(obtenerBD)):
    # 1. Buscar al usuario en la base de datos usando la entidad User
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    # 2. Mapeo de nombres para que coincidan con el ENUM de MySQL
    # Unity manda strings como "Baritono" o "Bajo", MySQL espera "BARITONE" o "BASS"
    tessitura_mapeada = request.tessitura.upper()
    
    # Mapeos específicos si es necesario
    mapeo = {
        "BARITONO": "BARITONE",
        "BAJO": "BASS",
        "MEZZO SOPRANO": "MEZZO_SOPRANO",
        "CONTRALTO": "CONTRALTO",
        "SOPRANO": "SOPRANO",
        "TENOR": "TENOR"
    }
    
    # Si el valor está en el mapeo, lo cambiamos, si no, usamos el original en mayúsculas
    user.tessitura = mapeo.get(tessitura_mapeada, tessitura_mapeada)

    # 3. Guardar cambios
    try:
        db.commit()
        db.refresh(user)
        print(f"✅ DB Actualizada: Usuario {user.username} ahora es {user.tessitura}")
        return {"status": "success", "new_tessitura": user.tessitura}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al guardar en DB: {str(e)}")
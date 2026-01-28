import os
from datetime import datetime, timedelta
from typing import Optional
from jose import jwt
from passlib.context import CryptContext

# --- CONFIGURACIÓN DE CONTRASEÑAS ---
# Bcrypt es el estándar para convertir claves en hashes seguros
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# --- CONFIGURACIÓN DE JWT (Cargada desde .env) ---
# La SECRET_KEY es la "firma" del servidor. Si alguien la tiene, puede falsificar sesiones.
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")) # 24h por defecto

def get_password_hash(password: str) -> str:
    """Convierte la clave del usuario en un hash ilegible para la DB."""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Compara la clave que mete el usuario con el hash guardado."""
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Genera un token JWT firmado.
    El 'data' suele contener el ID del usuario como 'sub'.
    """
    to_encode = data.copy()
    
    # Calculamos cuándo caduca el token
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    # Añadimos la expiración al cuerpo del token (claim 'exp')
    to_encode.update({"exp": expire})
    
    # Firmamos el JSON con nuestra llave secreta
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
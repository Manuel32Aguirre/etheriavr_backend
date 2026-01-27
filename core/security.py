from passlib.context import CryptContext

# Configuramos el algoritmo. Bcrypt es seguro y estándar
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    #Convertimos en un hash ilegible
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    #Compara la clave que mete el usuario con la que está en la DB
    return pwd_context.verify(plain_password, hashed_password)
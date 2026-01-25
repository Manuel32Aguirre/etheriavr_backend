import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

# 1. Cargamos el .env que está en la raíz
load_dotenv()

# 2. Extraemos las credenciales (Se mapean directo desde tu .env)
DB_USER = os.getenv("MYSQL_USER")
DB_PASS = os.getenv("MYSQL_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("MYSQL_DATABASE")


DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(
    DATABASE_URL, 
    pool_pre_ping=True
)

# 5. Creador de Sesiones
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 6. Clase Base para tus modelos (User, Song, etc.)
Base = declarative_base()

# 7. Dependencia para los Controllers de FastAPI
def get_db():
    """Generador de sesiones de base de datos para los endpoints"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
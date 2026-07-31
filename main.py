from sqlalchemy import inspect, text # Importante para ejecutar SQL puro
from config.connection import engine, Base, SessionLocal # <--- Agrega SessionLocal aquí
from dotenv import load_dotenv
from config.broadcast_service import start_udp_beacon
load_dotenv()

import os
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware 

from config.connection import engine, Base
from controllers import UserController, SongController, UserConfigurationController, PracticeSessionController


def _as_bool(value, default=False):
    if value is None:
        return default
    return str(value).strip().lower() in {"1", "true", "yes", "on"}

APP_HOST = os.getenv("APP_HOST")
APP_PORT = int(os.getenv("APP_PORT"))
DEBUG_MODE = _as_bool(os.getenv("DEBUG_MODE"), default=False)
IS_DEPLOYMENT = _as_bool(os.getenv("IS_DEPLOYMENT"), default=False)
ENABLE_UDP_BEACON = _as_bool(os.getenv("ENABLE_UDP_BEACON"), default=not IS_DEPLOYMENT)

Base.metadata.create_all(bind=engine)


def asegurar_campos_confirmacion_correo():
    """Añade los campos de confirmación a instalaciones que ya tenían la tabla users."""
    existing_columns = {
        column["name"] for column in inspect(engine).get_columns("users")
    }
    required_columns = {
        "email_verified": "BOOLEAN NOT NULL DEFAULT FALSE",
        "email_verification_code_hash": "VARCHAR(255) NULL",
        "email_verification_expires_at": "DATETIME NULL",
    }

    with engine.begin() as connection:
        for column_name, definition in required_columns.items():
            if column_name not in existing_columns:
                connection.execute(
                    text(f"ALTER TABLE users ADD COLUMN {column_name} {definition}")
                )


asegurar_campos_confirmacion_correo()


def ejecutar_import_sql():
    db = SessionLocal()
    try:
        canciones_existen = db.execute(text("SELECT 1 FROM songs LIMIT 1")).fetchone()
        
        if not canciones_existen:
            print("Ejecutando import.sql...")
            with open("import.sql", encoding="utf-8") as f:
                consultas = f.read().split(";")
                for consulta in consultas:
                    if consulta.strip():
                        db.execute(text(consulta))
            db.commit()
            print("Datos iniciales cargados.")
    except Exception as e:
        print(f"Error al cargar import.sql: {e}")
        db.rollback()
    finally:
        db.close()

# Llamamos a la función
ejecutar_import_sql()


app = FastAPI(
    title="EtheriaVR Backend",
    version="1.0",
    description="API para el sistema de entrenamiento musical en VR"
)

# Ahora sí, el middleware funcionará sin errores
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(UserController.router)
app.include_router(SongController.router) # <--- ¡ESTA ES LA CLAVE!
app.include_router(UserConfigurationController.router)
app.include_router(PracticeSessionController.router)


@app.get("/")
def root():
    return {
        "message": "Servidor EtheriaVR activo",
        "status": "running"
    }

@app.get("/health")
def health_check():
    return {"status": "healthy"}

def main():
    if ENABLE_UDP_BEACON:
        start_udp_beacon(APP_PORT)
    else:
        print("[Startup] UDP beacon deshabilitado por configuracion de despliegue.")

    uvicorn.run(
        "main:app", 
        host=APP_HOST,
        port=APP_PORT,
        reload=DEBUG_MODE
    )

if __name__ == "__main__":
    main()
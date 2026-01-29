from sqlalchemy import text # Importante para ejecutar SQL puro
from config.connection import engine, Base, SessionLocal # <--- Agrega SessionLocal aquí
from dotenv import load_dotenv
load_dotenv()

import os
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware 

from config.connection import engine, Base
from controllers import UserController, SongController

APP_HOST = os.getenv("APP_HOST")
APP_PORT = int(os.getenv("APP_PORT"))
DEBUG_MODE = os.getenv("DEBUG_MODE").lower() == "true"

Base.metadata.create_all(bind=engine)


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
    uvicorn.run(
        "main:app", 
        host=APP_HOST,
        port=APP_PORT,
        reload=DEBUG_MODE
    )

if __name__ == "__main__":
    main()
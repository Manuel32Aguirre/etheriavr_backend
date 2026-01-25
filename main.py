# Cargar variables de entorno
from dotenv import load_dotenv
load_dotenv()

import os
import uvicorn
from fastapi import FastAPI
from config.connection import engine, Base
from models.entities.User import User

APP_HOST = os.getenv("APP_HOST")
APP_PORT = int(os.getenv("APP_PORT"))
DEBUG_MODE = os.getenv("DEBUG_MODE").lower() == "true"

# --- LÓGICA DDL (Estilo Hibernate Auto) ---
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="EtheriaVR Backend",
    version="1.0",
    description="API para el sistema de entrenamiento musical en VR"
)

# Registrar routers
#app.include_router(user_controller.router)

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
    # El comando "main:app" permite que el reload funcione correctamente en Docker
    uvicorn.run(
        "main:app", 
        host=APP_HOST,
        port=APP_PORT,
        reload=DEBUG_MODE
    )

if __name__ == "__main__":
    main()
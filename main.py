from dotenv import load_dotenv
load_dotenv()

import os
import uvicorn
from fastapi import FastAPI
# ESTA ES LA LÍNEA QUE TE FALTA:
from fastapi.middleware.cors import CORSMiddleware 

from config.connection import engine, Base
from controllers import UserController

APP_HOST = os.getenv("APP_HOST")
APP_PORT = int(os.getenv("APP_PORT"))
DEBUG_MODE = os.getenv("DEBUG_MODE").lower() == "true"

Base.metadata.create_all(bind=engine)

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
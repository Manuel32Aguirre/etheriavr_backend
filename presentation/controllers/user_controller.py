from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from application.use_cases.RegisterUserUseCase import RegisterUserUseCase
from infrastructure.database.connection import get_db
from infrastructure.database.repositories.user_repository_sqlalchemy import UserRepositorySQLAlchemy
from presentation.controllers.dtos.user_post_dto import RegisterUserDTO

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/register")
def register_user(request: RegisterUserDTO, db: Session = Depends(get_db)):
    user_repository = UserRepositorySQLAlchemy(db)
    use_case = RegisterUserUseCase(user_repository)

    try:
        created_user = use_case.execute(request.username, request.email, request.password)
        return {
            "id": created_user.user_id,
            "username": created_user.username,
            "email": created_user.email
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")

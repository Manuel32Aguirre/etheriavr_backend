from domain.entities.user import User
from domain.repositories.IUserRepository import IUserRepository

class RegisterUserUseCase: 

    def __init__(self, user_repository: IUserRepository):
        self.user_repository = user_repository

    def execute(self, username: str, email: str, password_hash: str) -> User:
        existing_user = self.user_repository.get_user_by_email(email)
        
        #Regla de negocio: No se puede registrar un usuario con un correo ya existente
        if existing_user:
            raise ValueError(f"El usuario con el correo {email} ya existe.")
        
        new_user = User(username=username, email=email, password_hash=password_hash)

        created_user = self.user_repository.register_user(new_user)

        return created_user
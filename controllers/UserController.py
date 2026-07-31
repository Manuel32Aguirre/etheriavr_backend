from html import escape
from typing import Optional

from fastapi import APIRouter, Depends, Form, status, HTTPException
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from config.connection import obtenerBD
from models.entities.User import User  # IMPORTANTE: Asegúrate de que esta ruta sea correcta
from models.dto.request.UserCreateRequest import UserCreateRequest
from models.dto.request.UserTessituraRequest import UserTessituraRequest
from models.dto.request.UserLoginRequest import UserLoginRequest
from models.dto.response.UserCreateResponse import UserCreateResponse
from models.dto.response.UserLoginResponse import UserLoginResponse
from models.dto.request.EmailVerificationRequest import EmailVerificationRequest
from models.dto.request.ResendEmailVerificationRequest import ResendEmailVerificationRequest
from services.UserService import UserService
from core.security import get_current_user

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


@router.post("/users/email-verification", status_code=status.HTTP_200_OK)
def verify_email(request: EmailVerificationRequest, db: Session = Depends(obtenerBD)):
    usuarioServicio = UserService(db)
    usuarioServicio.verificarCorreo(request)
    return {"message": "Correo electrónico confirmado correctamente."}


@router.post("/users/email-verification/resend", status_code=status.HTTP_200_OK)
def resend_email_verification(
    request: ResendEmailVerificationRequest,
    db: Session = Depends(obtenerBD),
):
    usuarioServicio = UserService(db)
    usuarioServicio.reenviarCodigoConfirmacion(request.email)
    return {"message": "Si existe una cuenta pendiente, se envió un nuevo código de confirmación."}


def _verification_page(email: str = "", message: str = "", is_error: bool = False) -> str:
    safe_email = escape(email, quote=True)
    safe_message = escape(message)
    message_html = ""
    if message:
        message_class = "error" if is_error else "success"
        message_html = f'<p class="{message_class}">{safe_message}</p>'

    return f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Confirmar correo | EtheriaVR</title>
        <style>
            * {{ box-sizing: border-box; }}
            body {{
                margin: 0; min-height: 100vh; display: grid; place-items: center;
                background: linear-gradient(135deg, #101827, #33245e);
                color: #e5e7eb; font-family: Arial, sans-serif; padding: 24px;
            }}
            main {{
                width: min(100%, 420px); background: rgba(17, 24, 39, .96);
                border: 1px solid #5b4b8a; border-radius: 16px; padding: 32px;
                box-shadow: 0 24px 60px rgba(0, 0, 0, .35);
            }}
            h1 {{ margin-top: 0; font-size: 26px; }}
            p {{ color: #cbd5e1; line-height: 1.5; }}
            label {{ display: block; font-size: 14px; margin: 18px 0 6px; }}
            input {{
                width: 100%; padding: 12px; border: 1px solid #64748b; border-radius: 8px;
                background: #0f172a; color: #f8fafc; font-size: 16px;
            }}
            input[name="code"] {{ letter-spacing: 7px; text-align: center; font-weight: bold; }}
            button {{
                width: 100%; border: 0; border-radius: 8px; margin-top: 24px; padding: 13px;
                background: #8b5cf6; color: white; cursor: pointer; font-size: 16px; font-weight: bold;
            }}
            button:hover {{ background: #7c3aed; }}
            .success, .error {{ padding: 10px; border-radius: 8px; }}
            .success {{ background: #14532d; color: #dcfce7; }}
            .error {{ background: #7f1d1d; color: #fee2e2; }}
        </style>
    </head>
    <body>
        <main>
            <h1>Confirma tu correo</h1>
            <p>Escribe el código de seis dígitos enviado a tu correo electrónico.</p>
            {message_html}
            <form method="post" action="/api/verify-email">
                <label for="email">Correo electrónico</label>
                <input id="email" name="email" type="email" value="{safe_email}" required>
                <label for="code">Código de confirmación</label>
                <input id="code" name="code" type="text" inputmode="numeric" pattern="[0-9]{{6}}" maxlength="6" required autofocus>
                <button type="submit">Confirmar correo</button>
            </form>
        </main>
    </body>
    </html>
    """


@router.get("/verify-email", response_class=HTMLResponse, include_in_schema=False)
def verify_email_page(email: Optional[str] = None):
    return HTMLResponse(_verification_page(email or ""))


@router.post("/verify-email", response_class=HTMLResponse, include_in_schema=False)
def submit_verify_email_page(
    email: str = Form(...),
    code: str = Form(...),
    db: Session = Depends(obtenerBD),
):
    try:
        request = EmailVerificationRequest(email=email, code=code)
        UserService(db).verificarCorreo(request)
        return HTMLResponse(
            _verification_page(email, "Tu correo ha sido confirmado. Ya puedes iniciar sesión."),
            status_code=status.HTTP_200_OK,
        )
    except HTTPException as exc:
        return HTMLResponse(
            _verification_page(email, str(exc.detail), is_error=True),
            status_code=exc.status_code,
        )
    except ValueError:
        return HTMLResponse(
            _verification_page(email, "Introduce un correo y un código de seis dígitos válidos.", is_error=True),
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        )

# El endpoint de tessitura bajo el prefijo /api/users
@router.put("/users/{user_id}/tessitura")
async def update_tessitura(
    user_id: int,
    request: UserTessituraRequest,
    db: Session = Depends(obtenerBD),
    current_user: User = Depends(get_current_user),
):
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
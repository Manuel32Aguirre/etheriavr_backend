from html import escape
from typing import Optional

from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from config.connection import obtenerBD
from models.entities.User import User
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
    return {"message": "Si existe una cuenta pendiente, se envió un nuevo enlace de confirmación."}


def _result_page(
    ok: bool,
    title: str,
    message: str,
    email: str = "",
) -> str:
    safe_title = escape(title)
    safe_message = escape(message)
    if ok:
        box_color = "#dcfce7"
        text_color = "#14532d"
        icon = "✅"
        border = "#16a34a"
    else:
        box_color = "#fee2e2"
        text_color = "#7f1d1d"
        icon = "⚠️"
        border = "#dc2626"

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
                background: radial-gradient(circle at 50% 10%, #33245e 0%, #101827 60%);
                color: #e5e7eb; font-family: Arial, sans-serif; padding: 24px;
            }}
            main {{
                width: min(100%, 440px); background: rgba(17, 24, 39, .96);
                border: 1px solid #5b4b8a; border-radius: 20px; padding: 40px 32px;
                box-shadow: 0 24px 60px rgba(0, 0, 0, .45); text-align: center;
            }}
            .icon {{ font-size: 56px; line-height: 1; margin-bottom: 8px; }}
            h1 {{ margin: 8px 0 12px; font-size: 24px; color: #ffffff; }}
            .box {{
                margin-top: 20px; padding: 14px 16px; border-radius: 12px;
                background: {box_color}; color: {text_color};
                border: 1px solid {border}; font-size: 15px; line-height: 1.5; text-align: left;
            }}
            small {{ color: #9ca3af; display: block; margin-top: 20px; font-size: 13px; }}
        </style>
    </head>
    <body>
        <main>
            <div class="icon">{icon}</div>
            <h1>{safe_title}</h1>
            <div class="box">{safe_message}</div>
            <small>EtheriaVR · Confirmación de cuenta · {email}</small>
        </main>
    </body>
    </html>
    """


@router.get("/verify-email", response_class=HTMLResponse, include_in_schema=False)
def verify_email_page(
    email: Optional[str] = None,
    token: Optional[str] = None,
    db: Session = Depends(obtenerBD),
):
    if not email or not token:
        return HTMLResponse(
            _result_page(
                False,
                "Enlace incompleto",
                "El enlace de confirmación es inválido o está incompleto. Revisa tu correo.",
            ),
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    try:
        request = EmailVerificationRequest(email=email, token=token)
        UserService(db).verificarCorreo(request)
        return HTMLResponse(
            _result_page(
                True,
                "¡Correo confirmado!",
                "Tu cuenta ha sido verificada con éxito. Ya puedes cerrar esta "
                "página e iniciar sesión en EtheriaVR.",
                email,
            ),
            status_code=status.HTTP_200_OK,
        )
    except HTTPException as exc:
        return HTMLResponse(
            _result_page(
                False,
                "No se pudo confirmar",
                str(exc.detail),
                email,
            ),
            status_code=exc.status_code,
        )
    except ValueError:
        return HTMLResponse(
            _result_page(
                False,
                "Enlace inválido",
                "El enlace de confirmación no es válido.",
                email,
            ),
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
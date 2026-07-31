import os
import smtplib
from email.message import EmailMessage
from html import escape
from urllib.parse import quote

from fastapi import HTTPException, status
from dotenv import load_dotenv

load_dotenv()


class EmailService:
    @staticmethod
    def verification_code_expire_minutes() -> int:
        return int(os.getenv("EMAIL_VERIFICATION_CODE_EXPIRE_MINUTES", "15"))

    @staticmethod
    def send_verification_code(recipient: str, code: str) -> None:
        mail_from = os.getenv("MAIL_FROM")
        mail_username = os.getenv("MAIL_USERNAME", mail_from)
        mail_password = os.getenv("MAIL_PASSWORD")
        mail_server = os.getenv("MAIL_SERVER")
        mail_port = int(os.getenv("MAIL_PORT", "587"))
        app_public_url = os.getenv("APP_PUBLIC_URL", "http://localhost:8000").rstrip("/")

        if not all([mail_from, mail_username, mail_password, mail_server]):
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="El servicio de confirmación por correo no está configurado.",
            )

        verification_url = f"{app_public_url}/api/verify-email?email={quote(recipient)}"
        expires_in = EmailService.verification_code_expire_minutes()

        message = EmailMessage()
        message["Subject"] = "Confirma tu correo electrónico en EtheriaVR"
        message["From"] = mail_from
        message["To"] = recipient
        message.set_content(
            f"Tu código de confirmación es: {code}. "
            f"Expira en {expires_in} minutos. Abre {verification_url} para confirmarlo."
        )
        message.add_alternative(
            f"""
            <html>
              <body style="font-family: Arial, sans-serif; color: #1f2937;">
                <h2>Confirma tu correo electrónico</h2>
                <p>Tu código de confirmación es:</p>
                <p style="font-size: 28px; font-weight: bold; letter-spacing: 6px;">{escape(code)}</p>
                <p>El código expira en {expires_in} minutos.</p>
                <p><a href="{escape(verification_url, quote=True)}">Abrir página de confirmación</a></p>
              </body>
            </html>
            """,
            subtype="html",
        )

        try:
            with smtplib.SMTP(mail_server, mail_port, timeout=15) as server:
                server.ehlo()
                server.starttls()
                server.ehlo()
                server.login(mail_username, mail_password)
                server.send_message(message)
        except (OSError, smtplib.SMTPException) as exc:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="No se pudo enviar el código de confirmación. Inténtalo de nuevo más tarde.",
            ) from exc

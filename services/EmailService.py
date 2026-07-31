import os
import socket
import smtplib
import urllib.request
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
    def _obtener_ip_local() -> str:
        """Devuelve la IP local de la máquina que inicia una conexión saliente."""
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
                s.settimeout(2)
                s.connect(("8.8.8.8", 80))
                return s.getsockname()[0]
        except Exception:
            return "127.0.0.1"

    @staticmethod
    def _obtener_ip_publica() -> str | None:
        """Intenta obtener la IP pública de la máquina (útil en EC2)."""
        for url in ("http://checkip.amazonaws.com", "https://api.ipify.org"):
            try:
                with urllib.request.urlopen(url, timeout=5) as resp:
                    ip = resp.read().decode().strip()
                    if ip:
                        return ip
            except Exception:
                continue
        return None

    @staticmethod
    def _url_publica() -> str:
        """
        Devuelve la URL base pública del backend.
        Prioriza APP_PUBLIC_URL si está configurada con algo distinto a localhost.
        Si no, detecta automáticamente la IP pública (EC2) o la IP local.
        """
        app_public_url = (os.getenv("APP_PUBLIC_URL") or "").strip().rstrip("/")
        if not (
            not app_public_url
            or "localhost" in app_public_url.lower()
            or "127.0.0.1" in app_public_url
        ):
            return app_public_url

        port = os.getenv("APP_PORT", "8000")
        ip_publica = EmailService._obtener_ip_publica()
        if ip_publica:
            return f"http://{ip_publica}:{port}"

        ip_local = EmailService._obtener_ip_local()
        return f"http://{ip_local}:{port}"

    @staticmethod
    def send_verification_link(recipient: str, token: str) -> None:
        mail_from = os.getenv("MAIL_FROM")
        mail_username = os.getenv("MAIL_USERNAME", mail_from)
        mail_password = os.getenv("MAIL_PASSWORD")
        mail_server = os.getenv("MAIL_SERVER")
        mail_port = int(os.getenv("MAIL_PORT", "587"))

        if not all([mail_from, mail_username, mail_password, mail_server]):
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="El servicio de confirmación por correo no está configurado.",
            )

        base_url = EmailService._url_publica()
        verification_url = (
            f"{base_url}/api/verify-email"
            f"?email={quote(recipient)}&token={quote(token)}"
        )
        expires_in = EmailService.verification_code_expire_minutes()

        message = EmailMessage()
        message["Subject"] = "Confirma tu correo electrónico en EtheriaVR"
        message["From"] = mail_from
        message["To"] = recipient
        message.set_content(
            "Hola. Para confirmar tu correo en EtheriaVR, abre este enlace antes de que "
            f"expire ({expires_in} minutos):\n\n{verification_url}\n\n"
            "Si no solicitaste este correo, puedes ignorarlo."
        )
        message.add_alternative(
            (
                "<html>"
                "<body style=\"margin:0;padding:0;background-color:#f3f4f6;font-family:Arial,sans-serif;\">"
                "<div style=\"background-color:#f3f4f6;padding:32px 16px;\">"
                "<div style=\"max-width:480px;margin:0 auto;background:#ffffff;border-radius:16px;overflow:hidden;box-shadow:0 10px 30px rgba(0,0,0,.12);\">"
                "<div style=\"background:linear-gradient(135deg,#7c3aed,#4f46e5);padding:28px 24px;text-align:center;\">"
                "<h1 style=\"margin:0;color:#ffffff;font-size:22px;\">EtheriaVR</h1>"
                "</div>"
                "<div style=\"padding:32px 28px;color:#374151;\">"
                "<h2 style=\"margin:0 0 12px;color:#111827;font-size:20px;\">&#161;Casi est&#225; todo listo!</h2>"
                "<p style=\"margin:0 0 20px;font-size:15px;line-height:1.6;\">Para activar tu cuenta y poder iniciar "
                "sesi&#243;n, confirma tu direcci&#243;n de correo electr&#243;nico con el siguiente bot&#243;n.</p>"
                "<div style=\"text-align:center;padding:8px 0 24px;\">"
                "<a href=\"" + escape(verification_url, quote=True) + "\" target=\"_blank\" style=\"display:inline-block;"
                "background:linear-gradient(135deg,#7c3aed,#4f46e5);color:#ffffff;text-decoration:none;padding:14px 32px;"
                "border-radius:10px;font-weight:bold;font-size:15px;\">Confirmar mi correo</a>"
                "</div>"
                "<p style=\"margin:0;font-size:13px;color:#6b7280;line-height:1.6;\">Este enlace expira en "
                + str(expires_in)
                + " minutos. Si no solicitaste este correo, ign&#243;ralo y tu cuenta permanecer&#225; segura.</p>"
                "</div>"
                "<div style=\"padding:16px 28px;background-color:#f9fafb;text-align:center;\">"
                "<p style=\"margin:0;font-size:12px;color:#9ca3af;\">&#169; EtheriaVR &middot; Entrenamiento musical "
                "en realidad virtual</p>"
                "</div>"
                "</div>"
                "</div>"
                "</body></html>"
            ),
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
                detail="No se pudo enviar el enlace de confirmación. Inténtelo de nuevo más tarde.",
            ) from exc
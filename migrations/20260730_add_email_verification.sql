-- Respaldo para aplicar manualmente en MySQL si el usuario de la aplicación no tiene permiso ALTER.
ALTER TABLE users
    ADD COLUMN email_verified BOOLEAN NOT NULL DEFAULT FALSE,
    ADD COLUMN email_verification_code_hash VARCHAR(255) NULL,
    ADD COLUMN email_verification_expires_at DATETIME NULL;

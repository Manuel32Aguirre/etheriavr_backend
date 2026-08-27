# EtheriaVR Backend — Referencia completa

**Stack:** FastAPI · SQLAlchemy · MySQL · JWT (Bearer)  
**Flujo:** `Controller → Service → DAO → DB` · `Mapper`: Request/Entity ↔ Response

---

## Controllers

### `UserController` — prefijo `/api`

| Método | Ruta | Auth | Recibe | Devuelve |
|--------|------|------|--------|----------|
| POST | `/users` | No | `UserCreateRequest` | `UserCreateResponse` (201) |
| POST | `/login` | No | `UserLoginRequest` | `UserLoginResponse` |
| POST | `/users/email-verification` | No | `EmailVerificationRequest` | `{ message }` |
| POST | `/users/email-verification/resend` | No | `ResendEmailVerificationRequest` | `{ message }` |
| GET | `/verify-email` | No | query: `email`, `token` | HTML |
| PUT | `/users/{user_id}/tessitura` | JWT | path: `user_id`, body: `UserTessituraRequest` | `{ status, new_tessitura }` |

### `SongController` — prefijo `/api/songs`

| Método | Ruta | Auth | Recibe | Devuelve |
|--------|------|------|--------|----------|
| GET | `/listar` | JWT | — | `list[SongResponse]` |

### `UserConfigurationController` — prefijo `/api/users`

| Método | Ruta | Auth | Recibe | Devuelve |
|--------|------|------|--------|----------|
| GET | `/{user_id}/configuration` | JWT + owner | path: `user_id` | `UserConfigurationResponse` |
| PUT | `/{user_id}/configuration` | JWT + owner | path: `user_id`, body: `UserConfigurationRequest` | `UserConfigurationResponse` |

### `PracticeSessionController` — prefijo `/api/practice-sessions`

| Método | Ruta | Auth | Recibe | Devuelve |
|--------|------|------|--------|----------|
| POST | `` | JWT | `PracticeSessionCreateRequest` (user_id se fuerza al autenticado) | `PracticeSessionResponse` (201) |
| GET | `/user/{user_id}` | JWT + owner | path: `user_id` | `list[PracticeSessionResponse]` |

---

## Services

### `UserService(db: Session)`

| Método | Recibe | Devuelve |
|--------|--------|----------|
| `registrarUsuario` | `UserCreateRequest` | `UserCreateResponse` |
| `loginUsuario` | `UserLoginRequest` | `UserLoginResponse` |
| `verificarCorreo` | `EmailVerificationRequest` | `None` |
| `reenviarCodigoConfirmacion` | `email: str` | `None` |

**Usa:** `UserDAO`, `UserMapper`, `UserConfigurationMapper`, `EmailService`, `core.security`

### `SongService(db: Session)`

| Método | Recibe | Devuelve |
|--------|--------|----------|
| `getAllSongs` | — | `list[SongResponse]` |

**Usa:** `SongDAO`, `SongMapper`

### `UserConfigurationService(db: Session)`

| Método | Recibe | Devuelve |
|--------|--------|----------|
| `obtenerConfiguracionUsuario` | `user_id: int` | `UserConfigurationResponse` |
| `guardarConfiguracionUsuario` | `user_id: int`, `UserConfigurationRequest` | `UserConfigurationResponse` |

**Usa:** `UserDAO`, `UserConfigurationDAO`, `UserConfigurationMapper`

### `PracticeSessionService(db: Session)`

| Método | Recibe | Devuelve |
|--------|--------|----------|
| `registrarSesionPractica` | `PracticeSessionCreateRequest` | `PracticeSessionResponse` |
| `obtenerSesionesPorUsuario` | `user_id: int` | `list[dict]` con scores + `global_score` |

**Usa:** `PracticeSessionDAO`, `UserDAO`, `SongDAO`, `PracticeSessionMapper`

### `EmailService` (estático)

| Método | Recibe | Devuelve |
|--------|--------|----------|
| `verification_code_expire_minutes` | — | `int` |
| `send_verification_link` | `recipient: str`, `token: str` | `None` |

---

## DAOs (repositorios)

### `UserDAO(db)`

| Método | Recibe | Devuelve |
|--------|--------|----------|
| `save` | `User` | `User` |
| `getByEmail` | `email: str` | `User \| None` (eager: `user_configuration`) |
| `getById` | `user_id: int` | `User \| None` (eager: `user_configuration`) |

### `SongDAO(db)`

| Método | Recibe | Devuelve |
|--------|--------|----------|
| `getAll` | — | `list[Song]` (eager: `artist`) |
| `getById` | `song_id: int` | `Song \| None` |
| `getByMode` | `mode: str` | `list[Song]` |

### `UserConfigurationDAO(db)`

| Método | Recibe | Devuelve |
|--------|--------|----------|
| `save` | `UserConfiguration` | `UserConfiguration` |
| `getByUserId` | `user_id: int` | `UserConfiguration \| None` |

### `PracticeSessionDAO(db)`

| Método | Recibe | Devuelve |
|--------|--------|----------|
| `save` | `PracticeSession` | `PracticeSession` (eager: `song`) |

---

## Mappers

### `UserMapper`

| Método | Entrada | Salida |
|--------|---------|--------|
| `toEntity` | `UserCreateRequest`, `password_hash`, `verification_code_hash`, `verification_expires_at` | `User` |
| `toDto` | `User` | `UserCreateResponse` |
| `toLoginDto` | `User`, `token: str` | `UserLoginResponse` |

### `SongMapper`

| Método | Entrada | Salida |
|--------|---------|--------|
| `toDto` | `Song` | `SongResponse` |

### `UserConfigurationMapper`

| Método | Entrada | Salida |
|--------|---------|--------|
| `toEntity` | `UserCreateRequest` | `UserConfiguration` |
| `toEntityFromRequest` | `user_id: int`, `UserConfigurationRequest` | `UserConfiguration` |
| `toDto` | `UserConfiguration` | `UserConfigurationResponse` |

### `PracticeSessionMapper`

| Método | Entrada | Salida |
|--------|---------|--------|
| `toEntity` | `PracticeSessionCreateRequest` | `PracticeSession` |
| `toDto` | `PracticeSession` | `PracticeSessionResponse` |

---

## DTOs — Request (body)

| Clase | Campos |
|-------|--------|
| `UserCreateRequest` | `username`, `email`, `password`, `confirm_password`, `midi_device_name?`, `audience_intensity` |
| `UserLoginRequest` | `email`, `password` |
| `EmailVerificationRequest` | `email`, `token` |
| `ResendEmailVerificationRequest` | `email` |
| `UserTessituraRequest` | `tessitura: str` |
| `UserConfigurationRequest` | `midi_device_name?`, `audience_intensity?` |
| `PracticeSessionCreateRequest` | `user_id`, `song_id`, `practice_datetime?`, `practice_mode`, `rhythm_score`, `harmony_score?`, `tuning_score?` |

## DTOs — Response

| Clase | Campos |
|-------|--------|
| `UserCreateResponse` | `id`, `username`, `email`, `tessitura?`, `email_verified`, `configuration?` |
| `UserLoginResponse` | `access_token`, `token_type`, `id`, `username`, `email`, `tessitura?`, `email_verified`, `configuration?` |
| `UserConfigurationResponse` | `user_id`, `midi_device_name?`, `audience_intensity` |
| `SongResponse` | `id`, `musical_genre`, `musical_key`, `title`, `duration`, `mode`, `tempo`, `file_path`, `artist_name` |
| `PracticeSessionResponse` | `id`, `user_id`, `song_id`, `song_title`, `practice_datetime`, `practice_mode`, `rhythm_score`, `harmony_score?`, `tuning_score?`, `global_score?` |

---

## Entities (tablas)

| Clase | Tabla | Campos |
|-------|-------|--------|
| `User` | `users` | `id`, `username`, `email`, `password_hash`, `tessitura?`, `email_verified`, `email_verification_code_hash?`, `email_verification_expires_at?` |
| `UserConfiguration` | `user_configurations` | `user_id` (PK/FK), `midi_device_name?`, `audience_intensity` |
| `Artist` | `artists` | `id`, `name` |
| `Song` | `songs` | `id`, `musical_genre`, `musical_key`, `title`, `duration`, `mode`, `tempo`, `file_path`, `artist_id` |
| `PracticeSession` | `practice_sessions` | `id`, `user_id`, `song_id`, `practice_datetime`, `practice_mode`, `rhythm_score`, `harmony_score?`, `tuning_score?` |

---

## Enums

| Enum | Valores |
|------|---------|
| `Tessitura` | `SOPRANO`, `MEZZO_SOPRANO`, `CONTRALTO`, `TENOR`, `BARITONE`, `BASS` |
| `Mode` | `PIANO`, `CANTO` |
| `AudienceIntensity` | `Bajo`, `Medio`, `Alto` |

---

## Core / Config

| Archivo | Qué hace |
|---------|----------|
| `core/security.py` | `get_password_hash`, `verify_password`, `create_access_token`, `get_current_user` (JWT Bearer) |
| `core/authorization.py` | `require_owner(user_id, current_user)` — anti-IDOR |
| `config/connection.py` | `engine`, `Base`, `SessionLocal`, `obtenerBD` |
| `config/broadcast_service.py` | `start_udp_beacon` — descubrimiento LAN |

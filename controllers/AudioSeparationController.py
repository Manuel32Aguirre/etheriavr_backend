from fastapi import APIRouter, File, Form, Header, UploadFile
from fastapi.responses import FileResponse

from services.AudioSeparationService import AudioSeparationService

router = APIRouter(prefix="/api/audio", tags=["Audio Separation"])
audio_separation_service = AudioSeparationService()


@router.post("/separate")
async def separate_audio(
    file: UploadFile = File(...),
    include_original: bool = Form(default=False),
    authorization: str | None = Header(default=None),
) -> FileResponse:
    return await audio_separation_service.separate_upload(
        upload=file,
        include_original=include_original,
        authorization=authorization,
    )

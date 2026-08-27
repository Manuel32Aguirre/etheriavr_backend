from __future__ import annotations

import asyncio
import json
import math
import os
import shutil
import subprocess
import tempfile
import threading
import zipfile
from pathlib import Path
from typing import Any

import demucs.api
import numpy as np
import soundfile as sf
import torch
from fastapi import HTTPException, UploadFile
from fastapi.concurrency import run_in_threadpool
from fastapi.responses import FileResponse
from starlette.background import BackgroundTask


MODEL_NAME = os.getenv("DEMUCS_MODEL", "htdemucs_ft")
DEVICE = os.getenv(
    "DEMUCS_DEVICE", "cuda" if torch.cuda.is_available() else "cpu"
)
SHIFTS = int(os.getenv("DEMUCS_SHIFTS", "2"))
OVERLAP = float(os.getenv("DEMUCS_OVERLAP", "0.5"))
MAX_UPLOAD_BYTES = int(os.getenv("MAX_UPLOAD_BYTES", str(200 * 1024 * 1024)))
SAFE_PEAK = float(os.getenv("SAFE_PEAK", "0.98"))
API_TOKEN = os.getenv("VOCAL_SEPARATION_TOKEN", "").strip()
CONTRACT_VERSION = 1
REQUIRED_STEMS = ("vocals", "drums", "bass", "other")

_separator: demucs.api.Separator | None = None
_separator_lock = threading.Lock()
_inference_gate = asyncio.Semaphore(1)


class AudioSeparationService:
    @staticmethod
    def health_payload() -> dict[str, Any]:
        return {
            "status": "healthy",
            "service": "etheriavr-backend",
            "vocal_separation": {
                "enabled": True,
                "model": MODEL_NAME,
                "device": DEVICE,
                "contract_version": CONTRACT_VERSION,
            },
        }

    @staticmethod
    def verify_token(authorization: str | None) -> None:
        if not API_TOKEN:
            return
        expected = f"Bearer {API_TOKEN}"
        if authorization != expected:
            raise HTTPException(401, "Token de separación inválido.")

    async def separate_upload(
        self,
        upload: UploadFile,
        include_original: bool,
        authorization: str | None,
    ) -> FileResponse:
        self.verify_token(authorization)

        if not upload.filename:
            raise HTTPException(400, "Archivo de audio requerido.")

        work_dir = Path(tempfile.mkdtemp(prefix="etheria_stems_"))
        suffix = Path(upload.filename).suffix.lower() or ".audio"
        input_path = work_dir / f"original{suffix}"

        try:
            await self._save_upload(upload, input_path)

            async with _inference_gate:
                package_path = await run_in_threadpool(
                    self._separate_and_package,
                    input_path,
                    work_dir,
                    include_original,
                )

            return FileResponse(
                path=package_path,
                media_type="application/zip",
                filename="etheria_stems.zip",
                background=BackgroundTask(shutil.rmtree, work_dir, ignore_errors=True),
            )
        except HTTPException:
            shutil.rmtree(work_dir, ignore_errors=True)
            raise
        except Exception as exc:
            shutil.rmtree(work_dir, ignore_errors=True)
            raise HTTPException(500, f"Separación IA falló: {exc}") from exc

    async def _save_upload(self, upload: UploadFile, destination: Path) -> None:
        total = 0
        with destination.open("wb") as output:
            while chunk := await upload.read(1024 * 1024):
                total += len(chunk)
                if total > MAX_UPLOAD_BYTES:
                    raise HTTPException(413, "El archivo excede el tamaño permitido.")
                output.write(chunk)

        if total < 1024:
            raise HTTPException(400, "El archivo de audio está vacío o corrupto.")

    def _separate_and_package(
        self, input_path: Path, work_dir: Path, include_original: bool
    ) -> Path:
        separator = self._get_separator()
        input_info = self._probe_audio(input_path)

        original, stems = separator.separate_audio_file(input_path)

        missing = [name for name in REQUIRED_STEMS if name not in stems]
        if missing:
            raise RuntimeError(f"El modelo no devolvió stems requeridos: {missing}")

        arrays: dict[str, np.ndarray] = {
            name: self._tensor_to_channels_last(stems[name]) for name in REQUIRED_STEMS
        }
        original_array = self._tensor_to_channels_last(original)

        self._validate_shapes(arrays)
        self._validate_finite(arrays)

        instrumental = arrays["drums"] + arrays["bass"] + arrays["other"]
        arrays["instrumental"] = instrumental

        raw_reconstruction = (
            arrays["drums"]
            + arrays["bass"]
            + arrays["other"]
            + arrays["vocals"]
        )
        compare_frames = min(raw_reconstruction.shape[0], original_array.shape[0])
        reconstruction_error_rms = self._rms(
            raw_reconstruction[:compare_frames] - original_array[:compare_frames]
        )

        raw_peaks = {name: self._peak(audio) for name, audio in arrays.items()}
        instrumental_names = ("drums", "bass", "other", "instrumental")
        instrumental_max_peak = max(raw_peaks[name] for name in instrumental_names)
        mix_gain = (
            min(1.0, SAFE_PEAK / instrumental_max_peak)
            if instrumental_max_peak > 0
            else 1.0
        )
        for name in instrumental_names:
            arrays[name] = arrays[name] * mix_gain

        vocals_peak = raw_peaks["vocals"]
        vocals_gain = (
            min(1.0, SAFE_PEAK / vocals_peak) if vocals_peak > 0 else 1.0
        )
        arrays["vocals"] = arrays["vocals"] * vocals_gain

        output_peak = self._peak(arrays["instrumental"])
        if output_peak > 1.0:
            raise RuntimeError(f"Clipping detectado antes de exportar: peak={output_peak}")

        output_dir = work_dir / "stems"
        output_dir.mkdir(parents=True, exist_ok=True)
        sample_rate = int(separator.samplerate)

        for name in (*REQUIRED_STEMS, "instrumental"):
            sf.write(
                output_dir / f"{name}.wav",
                arrays[name],
                sample_rate,
                format="WAV",
                subtype="PCM_16",
            )

        original_peak = self._peak(original_array)
        original_gain = min(1.0, SAFE_PEAK / original_peak) if original_peak > 0 else 1.0
        if include_original:
            sf.write(
                output_dir / "original.wav",
                original_array * original_gain,
                sample_rate,
                format="WAV",
                subtype="PCM_16",
            )

        frame_count = arrays["instrumental"].shape[0]
        duration_seconds = frame_count / sample_rate
        manifest = {
            "contract_version": CONTRACT_VERSION,
            "method": "ai_4stem_sum",
            "model": MODEL_NAME,
            "instrumental_formula": "drums+bass+other",
            "input_sample_rate": self._safe_int(input_info.get("sample_rate", 0)),
            "input_channels": self._safe_int(input_info.get("channels", 0)),
            "input_codec": str(input_info.get("codec_name", "unknown")),
            "input_bitrate": self._safe_int(input_info.get("bit_rate", 0)),
            "output_sample_rate": sample_rate,
            "output_channels": int(arrays["instrumental"].shape[1]),
            "output_bit_depth": 16,
            "output_codec": "PCM_S16LE",
            "output_bitrate": sample_rate * 2 * 16,
            "duration_seconds": duration_seconds,
            "mix_gain": mix_gain,
            "vocals_gain": vocals_gain,
            "instrumental_peak": output_peak,
            "raw_peaks": raw_peaks,
            "original_export_gain": original_gain,
            "reconstruction_error_rms": reconstruction_error_rms,
            "post_processing": "none",
            "normalization": "attenuate_only_if_peak_exceeds_safe_peak",
            "safe_peak": SAFE_PEAK,
            "stems": list(REQUIRED_STEMS),
        }
        (output_dir / "manifest.json").write_text(
            json.dumps(manifest, indent=2), encoding="utf-8"
        )

        self._validate_exported_wavs(output_dir, sample_rate, duration_seconds)

        package_path = work_dir / "etheria_stems.zip"
        with zipfile.ZipFile(
            package_path, mode="w", compression=zipfile.ZIP_DEFLATED, compresslevel=3
        ) as archive:
            package_names = [
                "vocals.wav",
                "drums.wav",
                "bass.wav",
                "other.wav",
                "instrumental.wav",
                "manifest.json",
            ]
            if include_original:
                package_names.insert(0, "original.wav")
            for name in package_names:
                archive.write(output_dir / name, arcname=name)

        return package_path

    def _get_separator(self) -> demucs.api.Separator:
        global _separator
        if _separator is not None:
            return _separator

        with _separator_lock:
            if _separator is None:
                _separator = demucs.api.Separator(
                    model=MODEL_NAME,
                    device=DEVICE,
                    shifts=SHIFTS,
                    split=True,
                    overlap=OVERLAP,
                    jobs=1,
                    progress=False,
                )
        return _separator

    def _probe_audio(self, path: Path) -> dict[str, Any]:
        command = [
            "ffprobe",
            "-v",
            "error",
            "-select_streams",
            "a:0",
            "-show_entries",
            "stream=sample_rate,channels,duration,codec_name,bit_rate",
            "-of",
            "json",
            str(path),
        ]
        result = subprocess.run(command, capture_output=True, text=True, timeout=30)
        if result.returncode != 0:
            raise RuntimeError(f"ffprobe no pudo leer el audio: {result.stderr}")
        streams = json.loads(result.stdout).get("streams", [])
        if not streams:
            raise RuntimeError("El archivo no contiene una pista de audio.")
        return streams[0]

    @staticmethod
    def _tensor_to_channels_last(tensor: Any) -> np.ndarray:
        array = tensor.detach().cpu().float().numpy()
        if array.ndim != 2:
            raise RuntimeError(f"Forma de stem inesperada: {array.shape}")
        if array.shape[0] in (1, 2):
            array = array.T
        if array.shape[1] == 1:
            array = np.repeat(array, 2, axis=1)
        if array.shape[1] != 2:
            raise RuntimeError(f"Se esperaban 2 canales, llegaron {array.shape[1]}.")
        return np.ascontiguousarray(array, dtype=np.float32)

    @staticmethod
    def _validate_shapes(arrays: dict[str, np.ndarray]) -> None:
        shapes = {name: audio.shape for name, audio in arrays.items()}
        if len(set(shapes.values())) != 1:
            raise RuntimeError(f"Los stems no tienen la misma forma: {shapes}")

    @staticmethod
    def _validate_finite(arrays: dict[str, np.ndarray]) -> None:
        invalid = [name for name, audio in arrays.items() if not np.isfinite(audio).all()]
        if invalid:
            raise RuntimeError(f"Stems con NaN/Inf: {invalid}")

    @staticmethod
    def _validate_exported_wavs(
        output_dir: Path, sample_rate: int, duration_seconds: float
    ) -> None:
        for name in (*REQUIRED_STEMS, "instrumental"):
            info = sf.info(output_dir / f"{name}.wav")
            if info.samplerate != sample_rate or info.channels != 2:
                raise RuntimeError(f"Formato incorrecto en {name}.wav: {info}")
            if info.subtype != "PCM_16":
                raise RuntimeError(f"{name}.wav no es PCM 16-bit.")
            if abs(info.duration - duration_seconds) > 0.02:
                raise RuntimeError(f"Duración inconsistente en {name}.wav.")

    @staticmethod
    def _peak(audio: np.ndarray) -> float:
        return float(np.max(np.abs(audio))) if audio.size else 0.0

    @staticmethod
    def _rms(audio: np.ndarray) -> float:
        return float(math.sqrt(float(np.mean(np.square(audio))))) if audio.size else 0.0

    @staticmethod
    def _safe_int(value: Any) -> int:
        try:
            return int(value)
        except (TypeError, ValueError):
            return 0

from __future__ import annotations

import os
import tempfile
from functools import lru_cache
from pathlib import Path

from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from TTS.api import TTS

app = FastAPI(title="Voice Cloner API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

OUTPUT_DIR = Path(os.getenv("OUTPUT_DIR", "/tmp/outputs"))
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
MODEL_NAME = os.getenv("VOICE_MODEL", "tts_models/multilingual/multi-dataset/xtts_v2")


@lru_cache(maxsize=1)
def get_tts_model() -> TTS:
    return TTS(MODEL_NAME)


@app.get("/api/health")
def health() -> dict[str, str]:
    return {"status": "ok", "model": MODEL_NAME}


@app.post("/api/clone")
async def clone_voice(
    text: str = Form(...),
    language: str = Form("de"),
    reference_audio: UploadFile = File(...),
) -> FileResponse:
    suffix = Path(reference_audio.filename or "ref.wav").suffix or ".wav"

    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as ref_file:
        ref_file.write(await reference_audio.read())
        reference_path = Path(ref_file.name)

    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav", dir=OUTPUT_DIR) as out_file:
        output_path = Path(out_file.name)

    try:
        model = get_tts_model()
        model.tts_to_file(
            text=text,
            speaker_wav=str(reference_path),
            language=language,
            file_path=str(output_path),
        )
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=500, detail=f"Voice cloning failed: {exc}") from exc
    finally:
        reference_path.unlink(missing_ok=True)

    return FileResponse(path=output_path, media_type="audio/wav", filename="cloned_voice.wav")

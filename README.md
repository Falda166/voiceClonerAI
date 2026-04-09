# VoiceClonerAI (Python + Angular + Docker)

Dieses Projekt enthält:

- **Python/FastAPI Backend** für Voice-Cloning über Coqui XTTS
- **Angular Webapp** zum Hochladen einer Referenz-Audio und Eingeben von Text
- **Docker Compose** für den One-Command-Start

## Start

```bash
docker compose up --build
```

Dann öffnen:

- Frontend: http://localhost:8080
- Backend Health: http://localhost:8000/api/health

## Nutzung

1. Im Web-UI Referenz-Audio hochladen (WAV oder MP3).
2. Sprache und Zieltext eingeben.
3. **Stimme klonen** klicken.
4. Ergebnis als Audio abspielen.

## Hinweise

- Beim ersten Start lädt das Backendmodell (**xtts_v2**) herunter. Das kann dauern.
- CPU ist möglich, aber langsam. Für bessere Performance GPU-Setup verwenden.
- Nur Audio verwenden, für das du die Rechte hast.
- Das Backend konvertiert Uploads per `ffmpeg` nach WAV (24kHz/Mono), damit auch MP3 stabil funktioniert.
- Frontend-Nginx ist auf `client_max_body_size 0` gesetzt (kein Nginx-Uploadlimit). Wenn du weiterhin 413 bekommst: unbedingt neu bauen mit `docker compose up --build`.

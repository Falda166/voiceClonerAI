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

1. Im Web-UI Referenz-Audio hochladen.
2. Sprache und Zieltext eingeben.
3. **Stimme klonen** klicken.
4. Ergebnis als Audio abspielen.

## Hinweise

- Beim ersten Start lädt das Backendmodell (**xtts_v2**) herunter. Das kann dauern.
- CPU ist möglich, aber langsam. Für bessere Performance GPU-Setup verwenden.
- Nur Audio verwenden, für das du die Rechte hast.
- Upload-Limit im Frontend-Proxy (Nginx) ist auf **256 MB** gesetzt (`client_max_body_size`).

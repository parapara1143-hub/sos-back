# SOS BACKEND ENTERPRISE 1.2 (Full)
Stack: Flask 3, SQLAlchemy, JWT, Socket.IO, Limiter, PostgreSQL, Docker.
Módulos: Autenticação, Papéis, Incidentes (CRUD+anexos+RT), Chat, Notificações (FCM/Email),
Triangulação Wi‑Fi (APs cadastrados), Inspeções/Checklists, Webhooks Câmeras/Alarmes, Relatórios v2,
Rate-limit, Auditoria, Seeds e Backup.

## Setup rápido
1) `python -m venv .venv && . .venv/bin/activate` (Windows: `.venv\Scripts\activate`)
2) `pip install -r requirements.txt`
3) Configure `.env` (copie de `.env.example`)
4) `flask db upgrade`
5) `python scripts/seed_demo.py`
6) `python manage.py run` → http://localhost:8000

Docker: `docker compose up -d`
Login seed: owner@sos.local / 123456


## v1.5 FINAL — Additions
- JWT expirations configurable; refresh rotation with revocation table.
- Local uploads and S3 presigned support.
- Incident events → MTTA/MTTR analytics.
- PDFs for ASO and Evacuation reports (WeasyPrint).
- Pydantic validation (example on incident create).
- New routes: /api/files/*, /api/analytics/mtta_mttr, /api/pdf/*.

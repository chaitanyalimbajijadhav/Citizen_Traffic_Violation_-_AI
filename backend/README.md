# AI Smart Traffic Violation Backend

## Sprint 1
FastAPI, PostgreSQL/SQLAlchemy, users/reports baseline, JWT login,
report APIs, Redis connectivity and Swagger/OpenAPI.

## Sprint 2
Evidence metadata/upload validation, Redis AI job queue/status,
AI/OCR result contracts, controlled report status transitions,
role checks, review/audit records and backend tests.

## Setup

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

Copy `.env.example` to `.env` and set local values.

## Database

Create the PostgreSQL database first:

`traffic_db`

Then seed development users:

```bash
python -m app.db.seed
```

Development credentials:
- citizen / Citizen@123
- admin / Admin@123
- rto / Rto@12345

Do not use these credentials outside local development.

## Run

```bash
uvicorn app.main:app --reload
```

Swagger:
`http://127.0.0.1:8000/docs`

Health:
`GET /api/health`

## Test

```bash
pytest
```

## Sprint 2 API additions

- `POST /api/auth/register`
- `POST /api/evidence/reports/{report_id}`
- `POST /api/processing/reports/{report_id}/ai-job`
- `GET /api/processing/reports/{report_id}/status`
- `POST /api/processing/reports/{report_id}/ai-result`
- `POST /api/processing/reports/{report_id}/ocr-result`
- `POST /api/reviews/reports/{report_id}`

AI and OCR endpoints are integration contracts. They do not implement YOLO/OCR internally.

## Citizen registration

`POST /api/auth/register` accepts JSON with required `name`, `email`, and `password`
fields. The name must contain 1–100 characters, the email must be a valid
address of at most 100 characters, and the password must contain 8–100
characters. Email is normalized to lowercase and stored in the existing unique
`users.username` column because the current user schema has no separate email
column; users log in with that email as their username. The endpoint returns
`201 Created` with only `id`, `name`, `email`, and `role`. Duplicate email
registration returns `409 Conflict`.

No database migration is needed: registration uses the existing `users`
columns and username uniqueness constraint.

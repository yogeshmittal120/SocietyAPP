# SocietyAPP

Society-based resident help and earning network.

## MVP stack

- React Native mobile app
- FastAPI backend
- PostgreSQL
- SQLAlchemy + Alembic
- JWT authentication
- Society-level data isolation
- Points wallet and transaction ledger

## Repository structure

```
backend/
  app/
    api/
      routes/
    core/
    db/
    main.py
  requirements.txt
  .env.example
  .gitignore
```

## Backend setup

From the repository root:

```bash
cd backend
python -m venv .venv

# Windows
.venv\Scripts\activate

pip install -r requirements.txt

uvicorn app.main:app --reload
```

Open `http://127.0.0.1:8000/docs`.

The current backend contains only the application foundation and health endpoint. Authentication, models, migrations, society context, RLS integration, and business APIs will be added incrementally.

## Security

- Never commit `.env`.
- Never store plaintext passwords.
- Database access must remain behind the FastAPI backend.
- Society isolation must be enforced at the API/database layers.

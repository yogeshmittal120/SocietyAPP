# Database migrations

SocietyAPP uses Alembic to apply database schema changes.

## Production deployment

After the backend commit is deployed to Render, open the backend service Shell and run:

```bash
alembic upgrade head
```

The Render service's configured root directory should be `backend`, so run the command from that directory. If the Shell opens at the repository root instead, run:

```bash
cd backend
alembic upgrade head
```

For this release, revision `0006_add_user_full_name` adds a nullable `users.full_name` column so existing accounts remain valid. Registration now saves the full name and the profile API reads it.

Do not manually add the column in the Supabase SQL Editor and then run this migration; Alembic should own the schema change and revision tracking.

## Local development

Activate the backend virtual environment, configure `DATABASE_URL` and `JWT_SECRET_KEY`, then run `alembic upgrade head` from the backend directory.

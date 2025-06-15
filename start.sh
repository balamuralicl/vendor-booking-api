#!/bin/bash
set -e

echo "🐛 [start.sh] Script started"

echo "⏳ Waiting for PostgreSQL..."
until pg_isready -h db -p 5432 -U postgres; do
  sleep 1
done

echo "✅ PostgreSQL is ready. Initializing DB..."

# Add trace output
ls -l app/db/init_db.py
python -m app.db.init_db || echo "❌ init_db.py failed"

echo "🚀 Starting FastAPI app..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

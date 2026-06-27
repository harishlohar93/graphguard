#!/bin/bash
set -e

echo "Installing dependencies..."
pip install -r requirements.txt

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Running migrations..."
python manage.py migrate

echo "Seeding accounts..."
python manage.py seed_postgres

echo "Training model..."
python manage.py train_model

echo "Scoring accounts..."
python manage.py storescore_in_db

echo "Creating superuser..."
python manage.py createsuperuser --noinput --username admin --email admin@graphguard.com || true

echo "Build complete."
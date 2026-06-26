#!/bin/bash
set -e

echo "Python version: $(python --version)"

echo "Installing dependencies..."
pip install -r requirements.txt

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Running migrations..."
python manage.py migrate

echo "Seeding Neo4j graph..."
python manage.py seed_graph

echo "Syncing accounts to PostgreSQL..."
python manage.py sync_accounts

echo "Training ML model..."
python manage.py train_model

echo "Scoring all accounts..."
python manage.py storescore_in_db

echo "Creating superuser..."
python manage.py createsuperuser --noinput --username admin --email admin@graphguard.com || true

echo "Build complete."
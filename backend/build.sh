#!/bin/bash
set -e
echo "Python version: $(python --version)"

echo "Installing dependencies..."
pip install -r requirements.txt

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Running migrations..."
python manage.py migrate

echo "Creating superuser..."
python manage.py createsuperuser --noinput --username admin --email admin@graphguard.com || true

echo "Syncing accounts from Neo4j..."
python manage.py sync_accounts || true

echo "Seeding graph data..."
python manage.py seed_graph || true

echo "Training model..."
python manage.py train_model || true

echo "Scoring all accounts..."
python manage.py score_all || true

echo "Build complete."
#!/usr/bin/env bash
set -o errexit

echo "Installing dependencies..."
pip install -r requirements.txt

echo "Current directory contents:"
ls -la

echo "Checking Django installation and project setup..."
python -c "import django; print(f'Django version: {django.get_version()}')"

echo "Setting DJANGO_SETTINGS_MODULE..."
export DJANGO_SETTINGS_MODULE=MEB_HUB.settings

echo "Available Django commands:"
python manage.py help

echo "Attempting to collect static files..."
python manage.py collectstatic --noinput

echo "Running migrations..."
python manage.py migrate
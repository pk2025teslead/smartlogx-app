#!/usr/bin/env bash
# exit on error
set -o errexit

echo "Python version:"
python --version

echo "Pip version:"
pip --version

echo "Upgrading pip..."
pip install --upgrade pip

echo "Installing dependencies..."
pip install -r requirements.txt --no-cache-dir

echo "Collecting static files..."
python manage.py collectstatic --no-input

echo "Build completed successfully!"
echo "Note: Migrations and admin user creation will be done via web endpoint"
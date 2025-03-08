#!/usr/bin/env bash
# Exit on error
set -o errexit
set -o pipefail

# Modify this line as needed for your package manager (pip, poetry, etc.)
pip install -r requirements.txt

# Convert static asset files
python manage.py collectstatic --noinput

# Apply any outstanding database migrations
python manage.py migrate --noinput

# Create a default superuser for Django admin
DJANGO_SUPERUSER_USERNAME=admin DJANGO_SUPERUSER_EMAIL=admin@example.com DJANGO_SUPERUSER_PASSWORD=admin123 python manage.py createsuperuser --noinput

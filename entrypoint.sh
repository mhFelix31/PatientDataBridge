#!/bin/sh

# Run migrations
echo "Running migrations..."
python manage.py migrate

# Start the application
echo "Starting Django..."
exec python manage.py runserver 0.0.0.0:8000
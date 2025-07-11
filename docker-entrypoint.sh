#!/bin/bash
set -e
# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --no-input

#echo "Make migrations..."
#python manage.py makemigrations
echo "Installing node dependencies..."
npm install
#echo "Compiling node assets..."
npm run build
#echo "Running database migrations..."

echo "Applying migrations..."
python manage.py migrate
# Start the application
exec "$@"
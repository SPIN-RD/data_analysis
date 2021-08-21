#!/bin/sh
echo "start-server.sh script invoked"
echo "Running database migration..."
python /code/manage.py migrate

echo "Collecting static assets..."
python /code/manage.py collectstatic --noinput

echo "Running gunicorn server"
gunicorn --pythonpath backend spinrd.wsgi --bind 0.0.0.0:8000
#!/bin/bash

# Start Redis in the background (daemonized)
redis-server --daemonize yes

# Wait for Redis to fully start
until redis-cli ping; do
  echo "Waiting for Redis to start..."
  sleep 1
done

# Start Celery worker in the background
nohup celery -A explorebg worker --loglevel=info &

# Start Django server in the current terminal window
python manage.py runserver
#!/bin/bash

## Start Redis in the background (daemonized)
#redis-server --daemonize yes
#
## Wait for Redis to fully start
#until redis-cli ping; do
#  echo "Waiting for Redis to start..."
#  sleep 1
#done

# Start Celery worker in the background
nohup celery -A explorebg worker --loglevel=info &


#make migrations
python manage.py migrate


# Start Django server in the current terminal window
#python manage.py runserver
waitress-serve --port=8000 --threads=6 explorebg.wsgi:application

#!/bin/bash

/usr/wait-for-it.sh db:5432 -- echo "PostgreSQL is up"

python manage.py makemigrations
python manage.py migrate

exec gunicorn ltserLyudao.wsgi:application --bind 0.0.0.0:8200

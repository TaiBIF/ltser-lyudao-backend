#!/bin/bash
set -o errexit
set -o pipefail
set -o nounset

/usr/wait-for-it.sh db:5432 -- echo "PostgreSQL is up"

python manage.py migrate
python manage.py collectstatic --no-input

#exec gunicorn ltserLyudao.wsgi:application --bind 0.0.0.0:8000
#gunicorn ltserLyudao.wsgi:application --bind 0.0.0.0:8000

python manage.py runserver 0.0.0.0:8000

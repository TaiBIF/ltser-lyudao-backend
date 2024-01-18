#!/bin/bash
set -o errexit
set -o pipefail
set -o nounset

/usr/wait-for-it.sh db:5432 -- echo "PostgreSQL is up"

python manage.py migrate
python manage.py collectstatic --no-input

gunicorn --bind 0.0.0.0:8001 ltserLyudao.wsgi:application

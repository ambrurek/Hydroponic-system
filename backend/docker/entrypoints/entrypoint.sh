#!/bin/sh
python manage.py makemigrations
python manage.py migrate
python manage.py test
python -m black . 
exec "$@"
# We should migrate on startup in case there's been any db changes
python3 manage.py migrate
python manage.py runserver 0.0.0.0:8000
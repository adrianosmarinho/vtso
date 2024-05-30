# We should migrate on startup in case there's been any db changes
python3 manage.py migrate
# Ensure our OpenAPI schema is up to date
python manage.py spectacular --file schema.yaml
python manage.py runserver 0.0.0.0:8000
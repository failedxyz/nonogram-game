web: gunicorn --worker-class eventlet app:app --log-file -
dev: python manage.py db upgrade && python manage.py runserver
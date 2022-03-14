release: python manage.py migrate
web: gunicorn arike.wsgi --log-file -
worker: REMAP_SIGTERM=SIGQUIT celery -A arike.celery worker --loglevel=info
beat: REMAP_SIGTERM=SIGQUIT celery -A arike.celery beat --loglevel=info
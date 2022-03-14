release: python manage.py migrate
web: gunicorn arike.wsgi --log-file -
worker_only: celery -A arike worker --beat --loglevel=info
worker: REMAP_SIGTERM=SIGQUIT celery -A arike.celery worker --loglevel=info
beat: REMAP_SIGTERM=SIGQUIT celery -A arike.celery beat --loglevel=info
release: python manage.py migrate
web: gunicorn CZ3003CMS.wsgi --log-file -
email_scheduler: python email_scheduler.py 
release: python manage.py migrate
web: gunicorn CZ3003CMS.wsgi --log-file -
email_scheduler: python manage.py email_scheduler.py 
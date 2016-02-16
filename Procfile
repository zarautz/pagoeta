web: python manage.py migrate; python manage.py compilemessages; gunicorn pagoeta.wsgi:application --config gunicorn_cnf.py --bind 0.0.0.0:${PORT:-5000}

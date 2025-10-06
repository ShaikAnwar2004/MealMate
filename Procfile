release: cd meal_mate && python debug_db.py && python manage.py migrate && python manage.py collectstatic --noinput
web: gunicorn meal_mate.wsgi:application --chdir meal_mate --workers=2 --bind=0.0.0.0:$PORT



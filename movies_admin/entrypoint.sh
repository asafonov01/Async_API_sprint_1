while ! nc -z psql_movies 5432; do
      sleep 2;
done 
python manage.py migrate --no-input
python manage.py collectstatic --no-input

gunicorn -c gunicorn.conf.py

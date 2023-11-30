#! /usr/bin/env
# start-server.sh

if [ "$DEPLOY_ENV" = "STAGING" ] || [ "$DEPLOY_ENV" = "PRODUCTION" ]
then
 echo "Waiting for mysql..."
 while ! nc -z db 3306; do
   sleep 0.1
 done
 echo "MySQL started"
fi

echo "NGINX starting up dataweb server"
cd /projects
celery -A dataweb beat -l INFO --scheduler django_celery_beat.schedulers:DatabaseScheduler &
python manage.py migrate --noinput
python manage.py collectstatic --noinput
python manage.py init_admin
gunicorn dataweb.wsgi --user www-data --bind 0.0.0.0:8010 --workers 3 --timeout 90 &
memcached -u root &
nginx -g "daemon off;"

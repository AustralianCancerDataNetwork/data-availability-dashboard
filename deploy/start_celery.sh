#! /usr/bin/env
# start-server.sh
echo "celery starting up"
cd /projects
poetry run celery -A dashboard worker -l info

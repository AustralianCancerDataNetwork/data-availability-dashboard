FROM ubuntu:20.04

EXPOSE 8000
EXPOSE 8020

ENV PYTHONUNBUFFERED 1
ENV DEBIAN_FRONTEND=noninteractive
ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8

# Install libraries required by python-ldap as well as Redis server for celery and memcached for django-cache
RUN apt-get update && \
    apt-get -y install libsasl2-dev \
    libldap2-dev \
    libssl-dev \
    freetds-dev \
    libmysqlclient-dev \
    python3-pip \
    memcached \
    git \
    nginx \
    netcat \
    expect \
    apt-transport-https \
    ca-certificates -y \
    curl\
    python3-venv

RUN update-ca-certificates

WORKDIR /projects

# Copy requirements.txt to working directory
ADD poetry.lock .
ADD pyproject.toml .

RUN ln -s /usr/bin/python3 /usr/bin/python

# Install Python packages defined in requirements.txt
RUN python -m pip install --upgrade pip
RUN pip install poetry
RUN poetry export --without-hashes -f requirements.txt --output requirements.txt
RUN poetry config virtualenvs.create false

# Getting error when installing pyyaml=6.0 using poetry
RUN pip install --ignore-installed PyYAML==6.0 
RUN pip install -r requirements.txt

# Provide easy access to Django manage command
RUN printf '#!/bin/bash\ncd /projects\npython manage.py $@\n' > /usr/bin/manage && chmod +x /usr/bin/manage

WORKDIR /
COPY deploy/start_server.sh /
RUN chmod 755 /start_server.sh
RUN chown www-data /start_server.sh

COPY deploy/start_celery.sh /
RUN chmod 755 /start_celery.sh
RUN chown www-data /start_celery.sh

RUN mkdir /static
RUN chmod 755 /static
RUN chown www-data /static

RUN mkdir -p /var/lib/nginx
RUN chmod 755 /var/lib/nginx
RUN chown www-data /var/lib/nginx

RUN touch /run/nginx.pid 
RUN chown www-data /run/nginx.pid

ADD dashboard /projects/dashboard
ADD data_availability /projects/data_availability
ADD authenticate /projects/authenticate
ADD static /projects/static
ADD templates /projects/templates
ADD manage.py /projects/

RUN chmod 755 -R /projects
RUN chown www-data -R /projects

# Start Redis server for celery and memcached for Django cache
ENTRYPOINT memcached -u root

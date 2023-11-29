# Data Availabilty Dashboard

This repository contains the source code for a template data availability dashboard that was designed to inspect datasets within the AusCAT network.

## Project Structure

### Development

**NOTE**: For images that exist under the premium Dockerhub account, you'll need to login into the Dockerhub account on the local machine, by running `docker login`, then enter the username and password when promted.

**Docker**
The template can be deployed using docker. Via VSCode, you can setup the development containers
using the defined `.devcontainer.json` files and setup the application using its dockerfile-build image. This can be done
by:
1. Making sure that the extension "Remote-Containers" is installed.
2. Clicking on the bottom left green corner of VSC.
3. Select the option "Open folder in container". This will then open a VSC instance of the container and map it to your local repository.
Development and launching of the dashboard can now occur in this new VSC window.

Alternatively, you can spin up the containers by running the command:
```bash
docker-compose up -d
```

**Non-Docker approach**: This template can be ran without docker, by following these steps:

1. Install the poetry [tool](https://python-poetry.org/docs/).
2. Create a python virtual environment and activate it.
3. Navigate to `dashboard/` and run:

```bash
poetry install
```
This will install the python packages into your virtual environment

### Initial setup of the dashboard

1. To initialise the dashboard database, you can run the command:

```bash
python manage.py migrate
```

This will initialise the database based off of the models we've created for this project. The main models to ensure the dashboard runs accurately:
* `Config`: used to configure dashboard instances for your server. Multiple dashboards can exist where different insights can be generated, a unique URL is given and the source SQL database that the dashbaord visualises can be configured.
* `Feature`: used to define the different features you'd like to visualise on the dashboard. These are assigned to a specific `Config` and can be exported/imported as a JSON file for flexible management of features for your dashboard, as well as easy distribution if you'd like to replicate features accross different servers (ie. across different AusCAT centres).

2. Create a super user by running the command and selecting the appropriate options:

    ```bash
    python manage.py createsuperuser
    ```

This user will have access to the admin interface where the previously mentioned models can be created, as well as managing user account management.

3. The connection configuration to the database is controlled through the admin panel interface. Utlimately, this can be defined to point to real AusCAT databases for actual dashboard implementations. By default, this is not set. To set this, run the following command, navigate to `http://localhost:8080/admin` and login as a super user:

    ```bash
    python manage.py runserver
    ```

This will start the django server and launch the app. you can access the application using
[http://localhost:8000](http://localhost:8000)

4.  Once you have access to the admin panel, under the `data_availability` application, select `Config` and create a new instance. You can add the appropriate database credentials, as well as the SQL data query to extract the features you'd like to visualise on the dashboard and give this dashboard instance a unique URL. As mentioned, you can create multiple instances on your server.

5. You can create the features to be visualised by selecting the `Feature` application on the main admin page.

> Note: please ensure that you create at least *one* filter feaeture and *one* non-filter feature. A log will be produced on the server side when you first run it to remind you of this. 

### Simulation 
You can also run this dashboard using some artificial data:
1. Assuming you have a local database running to collect the artifical data, the data can be imported into the database by running the script `data_availability/data/import_csv_into_postgres.py`.

> WARNING: Please make sure this script does not run a function named `create_table` unless you are absolutely sure that you'd like to truncate the `medical` table in your database. By default this does not run, but please be aware before running this script

2. To initialise the Django local DB, run the command:

    ```bash
    python manage.py migrate
    ```

3. Create a super user for this development dashboard by running the command and selecting the appropriate options:

    ```bash
    python manage.py createsuperuser
    ```

4.  The connection configuration to the database is controlled through the admin panel interface. Utlimately, this can be defined to point to real AusCAT databases for actual dashboard implementations. By default, this is not set. To set this, run the following command, navigate to http://localhost:8080/admin and login as a super user:

    ```bash
    python manage.py runserver
    ```

## Troubleshooting

### Logs

The dashboard container will log to the standard output as is usual with Docker. These logs can be inspected within either Portainer or terminal to determine if dashboard is reporting any errors.

## Contact
For more information about the dashboard, please contact Daniel Al Mouiee (d.almouiee@unsw.edu.au).

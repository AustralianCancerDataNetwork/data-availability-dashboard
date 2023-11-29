"""Script to import a dummy "Medical" table into the local CAT_DB database.

    Usage:
        python import_csv_into_postgres.py
"""

import psycopg2
import yaml
import logging

logger = logging.getLogger(__name__)


def runSQLscript(sqlfilename, configfile):
    """
    Run SQL scripts in the sqlfile.

    Args:
        sqlfilename: SQL scripts.
        configfile: database configuration.
    """
    logger.info("Running SQL: %s", sqlfilename)
    # Open and read SQL file
    with open(sqlfilename, "r") as fd:
        sqlFile = fd.read()
    config = yaml.full_load(open(configfile))
    sqlCommands = sqlFile.split(";")
    # Connect to PostgreSQL database
    conn = psycopg2.connect(
        host=f'{config["hostname"]}',
        port=f'{config["portnumber"]}',
        database=f'{config["dbname"]}',
        user=f'{config["dbUser"]}',
        password=f'{config["dbPass"]}',
    )
    cursor = conn.cursor()
    conn.set_isolation_level(0)
    # Execute every command from the input file
    try:
        for command in sqlCommands[:-1]:
            cursor.execute(f"{command}")
            conn.commit()
    except (psycopg2.DatabaseError) as error:
        logger.error("Error while creating PostgreSQL table, '%s'", error)
    finally:
        if conn:
            cursor.close()
            conn.close()
            logger.info("Query/Script completed")
    return 0


def read_text_file(filename):
    """
    Read text file.
    Args:
        filename: the name of file you want to read.
    Returns:
        contents in the file.
    """
    # Open and read SQL file
    logger.info("Reading file: %s", filename)
    try:
        # Open and read SQL file
        with open(filename, "r") as fd:
            FileContents = fd.read()
        return FileContents
    except Exception as e:
        logger.error("Error while reading %s , '%s'", filename, e)


def import_csv(sqlfilename, csv_path, configfile):
    """
    Run a sql file, import a csv file to postgres, generate a table.

    Args:
        sqlfilename: SQL scripts.
        csv_path: the path where you want to import the csv file (refer to mount path in docker compose).
        configfile: database configuration.
    """
    config = yaml.full_load(open(configfile, "r"))
    # Connect to PostgreSQL database
    conn = psycopg2.connect(
        host=f'{config["hostname"]}',
        port=f'{config["portnumber"]}',
        database=f'{config["dbname"]}',
        user=f'{config["dbUser"]}',
        password=f'{config["dbPass"]}',
    )
    cursor = conn.cursor()

    # Read sql command from sqlfile
    s = read_text_file(sqlfilename)
    # Import csv file
    with open(csv_path) as file:
        cursor.copy_expert(s, file)

    try:
        logger.info(
            "Importing a csv file %s to postgres, generating a table...", csv_path
        )
        conn.commit()
    except Exception as e:
        logger.error("Error while importing a csv file to postgres, '%s'", e)


def main():
    # CREATION TABLE SCRIPT COMMENTED OUT, CAREFUL BEFORE RUNNING IT!
    # runSQLscript("create_table.sql", "cat_config.yml")
    import_csv("import_csv.sql", "medical.csv", "cat_config.yml")


main()

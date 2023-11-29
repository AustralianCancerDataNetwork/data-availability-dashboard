import logging
import psycopg2
import pandas as pd
from ..models import Config

LOGGER = logging.getLogger(__name__)


def query(query, url, *params):
    """ """
    LOGGER.info("Running query")

    # Connect to PostgreSQL database
    try:
        conf = Config.objects.filter(url_endpoint=url).first()
        host_ip = conf.db_servername
        port_num = conf.db_port
        db_name = conf.db_name
        username = conf.db_username
        password = conf.db_password

        conn = psycopg2.connect(
            host=host_ip,
            port=port_num,
            database=db_name,
            user=username,
            password=password,
        )
        data = pd.read_sql(query, conn)
        if conn:
            conn.close()
            print("Query/Script completed")
    except Exception as e:
        print(e)
        # Initial migration of database, placeholder pass
        data = pd.DataFrame()
        pass
    return data

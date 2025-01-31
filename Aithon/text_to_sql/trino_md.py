import trino
from .language_model import generate_chat_response

STARSHIP_CLIENT = trino.dbapi.connect(
    host='trino.nobroker.in',
    port=443,
    user='ds_starship',
    catalog='hive-v2',
    http_scheme='https',
    auth=trino.auth.BasicAuthentication("ds_starship", "2vEoGFs23w4htob"),
    session_properties={
        'query_max_run_time': '10m'  # Set the query time limit to 60 minutes
    })
import logging

# Create and configure logge

# Creating an object
logger = logging.getLogger()
import pandas as pd
# from commons.loggera import logger
# from commons.clients import STARSHIP_CLIENT
import requests
import json


class TrinoHandler(object):
    """
    Class to handle elasticsearch queries
    """
    _STARSHIP_CLIENT = STARSHIP_CLIENT

    @classmethod
    def fetch_data(cls, query, batch_size: int = 20000):
        """
        Fetch data from starship

        Args:
            query: SQL query to fetch data from starship tables
        """
        logger.info("Fetching data from Starship")

        cur = cls._STARSHIP_CLIENT.cursor()
        cur.execute(query)
        col_names = None
        presto_data = pd.DataFrame()
        file_no = 1
        while (True):
            rows = cur.fetchmany(batch_size)
            if not rows:
                break
            else:
                col_names = [part[0] for part in cur.description]
                presto_data = pd.concat([presto_data, pd.DataFrame(rows, columns=col_names)])
                print("Fetched upto : {}".format(str(file_no * batch_size)))
                file_no += 1
        return presto_data

    @classmethod
    def _get_starship_session(cls):
        """
        Get a session ID to access Starship
        """
        headers = {
            'Content-Type': 'application/json'
        }

        data = '{ "username": "metabase_api_user@nobroker.in", "password": "#1Starship" }'

        response = requests.post('http://192.168.0.53:3003/api/session', headers=headers, data=data)

        bb = response.json()

        return bb["id"]

    @classmethod
    def get_data_presto_from_question(cls, question_number):
        """
            Presto connector which returns data as Pandas dataframe. For Nobroker Two db
        """
        data = {"database": 7, "query": {"source-table": f"card__{question_number}"},
                "type": "query"}

        session_id = cls._get_starship_session()

        cookies = {
            'metabase.SESSION': session_id
        }

        resp = requests.post('http://192.168.0.53:3003/api/dataset/native',
                             cookies=cookies, json=data, verify=False)

        sql_query = json.loads(resp.text)["query"].replace(" LIMIT 1048575", "")

        cur = STARSHIP_CLIENT.cursor()
        cur.execute(sql_query)
        rows = cur.fetchall()
        col_names = [part[0] for part in cur.description]
        return pd.DataFrame(rows, columns=col_names)
def get_image_data(new_query):
    """
    Returns:
        data: Data containing vendors with url of selfie uploaded by them
    """
    data = TrinoHandler.fetch_data(query=new_query)

    return data

# if __name__ == "__main__":
#     # Test the get_image_data method
#     result = get_image_data()
#     print(result)
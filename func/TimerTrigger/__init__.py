import datetime
import logging
import os
import socket
import snowflake.connector
import azure.functions as func


def main(mytimer: func.TimerRequest) -> None:
    utc_timestamp = datetime.datetime.utcnow().replace(
        tzinfo=datetime.timezone.utc).isoformat()

    if mytimer.past_due:
        logging.info('The timer is past due!')

    conn = snowflake.connector.connect(
        user=os.environ.get('SF_USER'),
        password=os.environ.get('SF_PASS'),
        account=os.environ.get('SF_ACCOUNT'),
    )

    conn.cursor().execute("USE DATABASE SNOWFLAKE_SAMPLE_DATA")
    cur = conn.cursor()
    try:
        cur.execute("SHOW TABLES")
        for r in cur:
            logging.info(f"${r}")
    except Exception as e:
        logging.error(f"Something went wrong...\n${e}")
    finally:
        cur.close()
    logging.info('Python timer trigger function ran at %s', utc_timestamp)

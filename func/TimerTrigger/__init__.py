import datetime
import logging
import os
import socket
import snowflake.connector
import azure.functions as func
import time

def main(mytimer: func.TimerRequest) -> None:
    utc_timestamp_start = datetime.datetime.utcnow().replace(
        tzinfo=datetime.timezone.utc).isoformat()

    if mytimer.past_due:
        logging.info('The timer is past due!')
    logging.info('Python timer trigger function start at %s', utc_timestamp_start)

    try:
        conn = snowflake.connector.connect(
            user=os.environ.get('SF_USER'),
            password=os.environ.get('SF_PASS'),
            account=f"${os.environ.get('SF_ACCOUNT')}.privatelink",

            insecure_mode = True,
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
    except Exception as e:
        logging.error(f"Snowflake error: ${e}")

    utc_timestamp_end = datetime.datetime.utcnow().replace(
        tzinfo=datetime.timezone.utc).isoformat()
    logging.info('Python timer trigger function done %s', utc_timestamp_end)
    

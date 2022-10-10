import datetime
import logging
import os
import socket
import snowflake.connector
import azure.functions as func
import time

for logger_name in ['snowflake.connector']:
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)
    ch = logging.FileHandler('/tmp/python_connector.log')
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(logging.Formatter('%(asctime)s - %(threadName)s %(filename)s:%(lineno)d - %(funcName)s() - %(levelname)s - %(message)s'))
    logger.addHandler(ch)

class MySnowFlake():
    def __init__(self, account=f"{os.environ.get('SF_ACCOUNT')}.privatelink", user=os.environ.get('SF_USER'), password=os.environ.get('SF_PASS')):
        logging.info("MySnowFlake init...")
        self.conn = snowflake.connector.connect(
            user=user,
            password=password,
            account=account,
        )
        self.cursor = self.con.cursor()

    def close_con(self):
        logger.info("MySnowFlake Close Con...")
        self.cursor.close()
        self.con.close()

    def execute_query(self, query):
        try:
            logger.info(f"MySnowflake Execute Query: {query}")
            self.cursor.execute(query)
            results = self.cursor.fetchall()
        except Exception as e:
            logger.info(f"MySnowflake Execute Query Error: {e}")
        else:
            return results

    def do_stuff(self) -> None:
        self.execute_query("SHOW TABLES")
        self.execute_query("use warehouse myxsmallwarehouse")
        self.execute_query("use schema snowflake_sample_data.tpch_sf1")
        results = self.execute_query("SELECT l_returnflag, l_linestatus, sum(l_quantity) as sum_qty, sum(l_extendedprice) as sum_base_price, sum(l_extendedprice * (1-l_discount)) as sum_disc_price, sum(l_extendedprice * (1-l_discount) * (1+l_tax)) as sum_charge, avg(l_quantity) as avg_qty, avg(l_extendedprice) as avg_price, avg(l_discount) as avg_disc, count(*) as count_order FROM lineitem WHERE _shipdate <= dateadd(day, -90, to_date('1998-12-01')) GROUP BY l_returnflag, l_linestatus ORDER BY l_returnflag, l_linestatus")
        for r in results:
                logging.info(f"{r}")





def main(mytimer: func.TimerRequest) -> None:
    utc_timestamp_start = datetime.datetime.utcnow().replace(
        tzinfo=datetime.timezone.utc).isoformat()

    if mytimer.past_due:
        logging.info('The timer is past due!')
    logging.info('Python timer trigger function start at %s', utc_timestamp_start)

    try:
        msf = MySnowFlake()
        msf.do_stuff()
    except Exception as e:
        logging.error(f"Function error: {e}")

    utc_timestamp_end = datetime.datetime.utcnow().replace(
        tzinfo=datetime.timezone.utc).isoformat()
    logging.info('Python timer trigger function done %s', utc_timestamp_end)
    

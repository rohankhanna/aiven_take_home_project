from kafka import KafkaConsumer
import os
import json
import sys
from utils import *

if __name__ == "__main__":

    
    kafka_config = get_kafka_config()
    
    consumer = KafkaConsumer(kafka_config["topic"],
        bootstrap_servers = kafka_config["bootstrap_servers"],
        group_id ="monitoring",
        security_protocol="SSL",
        ssl_cafile=kafka_config["ssl_cafile"],
        ssl_certfile=kafka_config["ssl_certfile"],
        ssl_keyfile=kafka_config["ssl_keyfile"],
        auto_offset_reset="earliest",
        value_deserializer=lambda x: json.loads(x.decode('utf-8')),
        enable_auto_commit=True
    )

    data = []
    url_id_map = {'https://www.google.com':1,'https://www.reddit.com':2, 'https://github.com/':3} # replace with get request on table websites
    pg_connection = get_pg_connection()
    
    while True:
        messages = consumer.poll(timeout_ms=1000)
        if not messages.items():
            print(messages.items())
        for _, messages in messages.items():
            for message in messages:
                data.append(message.value)
                print(message.value)
        
        if data:
            try:
                cursor = pg_connection.cursor()
                for item in data:
                    # insert query based on the data received
                    cursor.execute("INSERT INTO availability (website_id, content) VALUES(%s, %s);", (url_id_map[item['url']],item['content']))
                cursor.close()
                pg_connection.commit()
            except (KeyboardInterrupt, Exception, psycopg2.Error) as error:
                pg_connection.close()
                raise RuntimeError(
                    "Error while inserting into PG database: {error}")

    
from kafka import KafkaConsumer
import os
import json
import sys
from utils import *

if __name__ == "__main__":

    kafka_config = get_kafka_config()

    consumer = KafkaConsumer(
        kafka_config["topic"],
        bootstrap_servers=kafka_config["bootstrap_servers"],
        group_id="monitoring",
        security_protocol="SSL",
        ssl_cafile=kafka_config["ssl_cafile"],
        ssl_certfile=kafka_config["ssl_certfile"],
        ssl_keyfile=kafka_config["ssl_keyfile"],
        auto_offset_reset="earliest",
        value_deserializer=lambda x: json.loads(x.decode("utf-8")),
        enable_auto_commit=True,
    )

    pg_connection = get_pg_connection()

    while True:
        data = []
        messages = consumer.poll(timeout_ms=1000)
        if not messages.items():
            print("No Messages")
        for _, messages in messages.items():
            for message in messages:
                data.append(message.value[0])
                print(message.value)

        if data:
            try:
                cursor = pg_connection.cursor()
                for item in data:
                    # insert query based on the data received
                    cursor.execute(
                        "INSERT INTO availability (website_id, available, status_code, response_time) VALUES(%s, %s, %s, %s);",
                        (
                            item["website_id"],
                            item["available"],
                            item["status_code"],
                            item["response_time"],
                        ),
                    )
                cursor.close()
                pg_connection.commit()
            except (KeyboardInterrupt, Exception, psycopg2.Error) as error:
                pg_connection.close()
                raise RuntimeError("Error while inserting into PG database: {error}")

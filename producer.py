# Import KafkaProducer from Kafka library
from kafka import KafkaProducer
import os
import json
import datetime
import random
from utils import *

urls = ['https://www.google.com', 'https://www.reddit.com', 'https://github.com/'];
def get_data():

    data = \
    [
        {
            "url" : random.choice(urls),
            "content" : str(datetime.datetime.now())*10
        }
    ]
    
    return data

if __name__ == "__main__":
    
    config = get_kafka_config()
    
    producer = KafkaProducer(
        bootstrap_servers = config["bootstrap_servers"],
        security_protocol="SSL",
        ssl_cafile=config["ssl_cafile"],
        ssl_certfile=config["ssl_certfile"],
        ssl_keyfile=config["ssl_keyfile"],
        value_serializer=lambda v: json.dumps(v).encode('ascii')
    )
    
    while True:
        for item in get_data():
                producer.send(config["topic"], item)
        producer.flush()
        print(print(datetime.datetime.now()))


    
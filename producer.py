from kafka import KafkaProducer
import os
import json
import datetime
import random
from utils import *
import time
import requests
import re
import sys


url_regex = {}
with open('url_regex.json', 'r') as file:
  url_regex = json.load(file)

def is_url_up(url, website_id):

    r = requests.get(url)
  
    data = \
    [
        {
            "website_id" : website_id,
            "available" : True if re.search(url_regex[url], r.text) else False,
            "status_code": r.status_code,
            "response_time": r.elapsed.total_seconds(),
            "timestamp": str(datetime.datetime.now())
        }
    ]
    
    return data

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Expecting a single argument: delay")
        exit()

    delay = int(sys.argv[1])
    pg_connection = get_pg_connection()
    cursor = pg_connection.cursor()
    website_ids = {}
    for url, _ in url_regex.items():
        cursor.execute("SELECT id from websites WHERE url = '"+url+"';")
        results = cursor.fetchall()
        if len(results) < 1:
            cursor.execute("INSERT INTO websites(url) VALUES ('"+url+"') RETURNING id;")
            results = cursor.fetchall()
        website_ids[url] = results[0][0]
    
    cursor.close()
    pg_connection.commit()
    
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
        time.sleep(delay)
        for url, website_id in website_ids.items():
            item = is_url_up(url, website_id)
            producer.send(config["topic"], item)
        producer.flush()
        print(print( "published at: ", datetime.datetime.now()))


    
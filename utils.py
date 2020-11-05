import os
import psycopg2


def get_kafka_config():
    return {
        "bootstrap_servers": [os.environ["KAFKA_URI"]],
        "ssl_cafile": os.environ["KAFKA_CA"],
        "ssl_certfile": os.environ["KAFKA_SERVICE_CERT"],
        "ssl_keyfile": os.environ["KAFKA_SERVICE_KEY"],
        "topic": os.environ["TOPIC_NAME"],
        "group_id": os.environ["GROUP_ID"],
    }


def get_postgres_config():
    return {"postgres_uri": os.environ.get("POSTGRES_URI")}


def get_pg_connection():
    postgres_config = get_postgres_config()
    try:
        connection = psycopg2.connect(postgres_config["postgres_uri"])
        return connection

    except (Exception, psycopg2.Error) as error:
        raise RuntimeError(f"Error connecting to PostgreSQL : {error}")

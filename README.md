# Aiven Take-home Project



## Installation

Install [Poetry](https://python-poetry.org/docs/)

We use Poetry to freeze dependencies to achieve determinism at build time, and to manage internal package dependencies. 

```bash
$ poetry shell # this will source the venv into your current shell session (Alternatively you may just create a python3 venv)
```

## Configuration and Setup

```bash
$ unzip credentials.zip # Unzip the given credentials.zip here .
$ # You may use your own database and kafka instance's credential files: service.key, service.cert, ca.pem and .env
$ source .env # This will load the config variables in bash.
$ python initialize.py # to load the schema onto the remote postgres db
```

## Usage

```bash
$ poetry install # to install dependencies. (Alternatively you may also do pip install -r requirements.txt)
```

In one shell session, run the consumer:

``` bash
# Run the Kafka event producer
$ python consumer.py
```

In another shell session, run the producer:
```bash
# in a separate shell session, enter the venv
$ poetry shell
$ source .env
# Run the Kafka event producer
$ python producer <delay> # the <delay> parameter is a value that represents how long must the producer wait
# before it scans for website availability (in seconds)
```



## Configuration:
Configurations are stored in ```.env``` for the actual remote db and kafka URI

The file ```url_regex.json``` describes the mapping between the url and the reqex search query we use to determine if a website is available or not.







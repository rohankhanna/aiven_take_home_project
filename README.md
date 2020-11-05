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
# Run the Kafka event Consumer
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


## Test Strategy:
The entire application is designed such that, each component is testable, both unit testable, and end-to-end testable. 

Unit testing the application may be done by means of applying patches and mocking KafkaProducer, KafkaConsumer and psycopg2's internal functions such that we may test the system individually, and independently of other components.

End to end testing may be done by sequentially by calling the producer and consumer functions, and passing run_once=True as parameters to these calls, then comparing the results of the test, along with testing for whether the database writes were successful. 

please refer the ```./tests``` folder to run ```test_end_to_end.py``` to run end-to-end tests. 
Please note that the tests will fail if there still exists some un-consumed data in the remote kafka instance. Please purge all data from the instance before use.











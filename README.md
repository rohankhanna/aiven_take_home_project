# aiven_take_home_project

Install:
Install Poetry from https://python-poetry.org/docs/
We use Poetry to freeze dependencies to achieve determinism at build time, and to manage internal package dependencies. 

Running the project:

	> Setup poetry venv:
		$ poetry install # to install dependencies. (Alternatively you may also do pip install -r requirements.txt)
		$ poetry shell # this will source the venv into your current shell session (Alternatively you may just create a python3 venv)

	> Load Config and Setup remote DB
		$ unzip credentials.zip # Alternatively, you may use your own database and kafka instance's credential files: service.key, service.cert, ca.pem and .env
		$ source .env # This will load the config variables in bash.
		$ python initialize.py # to load the schema onto the remote postgres db

	> Run the consumer:
		$ python consumer.py

	> Run the producer:
		# in a separate shell session, initalize the venv
		$ python producer <delay> # the <delay> parameter is a value that represents how long must the producer wait before it scans for website availability (in seconds)

Configuration:
	Configurations are stored in .env for the actual remote db and kafka URI
	the file url_regex.json describes the mapping between the url and the reqex search query we use to determine if a website is available or not.







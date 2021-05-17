# TCC

## Github setup (to-do)
create a token yata-yata-yata

## Installation
First, create a virtual environment to hold all of our python dependencies. To do so, you will need `virtualenv` so make sure you have it installed by running `pip install virtualenv`

Then, go to the project root and run `virtualenv .env` and activate it by running `\.env\Scripts\activate.bat`.

Now that you have a safe virtual environment set up, you can install the project dependencies by running `pip install -r requirements.txt`

Done! You are ready to run the project.

## Running
There are two ways to run the project: By hosting an API, that listens to HTTP requests or through the command line interface (CLI)

### CLI
To access the CLI, simply:
 - Go to the project root
 - Make sure that the virtual environment is activated (if not, run `\.env\Scripts\activate.bat`)
 - Run `python cli.py <yml_path> <github_user> <github_token>` replacing parameters between `<>` wherefor their appropriate values.

### API
To host the API:
 - Go to the project root
 - Make sure that the virtual environment is activated (if not, run `\.env\Scripts\activate.bat`)
 - Set the `FLASK_APP` environment variable by running `set FLASK_APP=flask.py`
 - Start the API's server by running `python -m flask run`

Now that you have the API up and running, make a POST to the `/upload` endpoint. The request must contain a `form-data` payload containing the following keys:
 - `file`: The YML that should be loaded
 - `github_user`: The Github username for which the project should be deployed
 - `github_token`: The Github personal access token for the above user

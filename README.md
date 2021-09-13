# TCC
The purpose of this project is to provide a tool for generating public documentation to a given process. To do so, it automatically generates a Jekyll project and deploys it into a Github Pages repository.

## Installation
First, create a virtual environment to hold all of our python dependencies. To do so, you will need `virtualenv` so make sure you have it installed by running `pip install virtualenv`

Then, go to the project root and run `virtualenv .env` and activate it by running `\.env\Scripts\activate.bat`.

Now that you have a safe virtual environment set up, you can install the project dependencies by running `pip install -r requirements.txt`

Last, you'll need to install Jekyll by running `gem install bundler jeykll` (if needed, more details on how to install Jekyll can be found [here](https://jekyllrb.com/docs/installation/))

## Process description
In order to submit a process, you will need to describe it in a YML file. An example for it can be found [here](https://github.com/alexpsilva/TCC/blob/main/mock.yml)

## Github setup
In order to host the generated documentation, you will need to provide access to a Github account. To do so, log into it, go to `Settings`, then `Developer settings`, then to the `Personal access tokens` section. There, click on `Generate new token`, give it a suiting name and the `public_repo` permisison.

## Running
There are two ways to run the project: By hosting an API, that listens to HTTP requests or through the command line interface (CLI)

### CLI
To access the CLI, simply:
 - Go to the project root
 - Make sure that the virtual environment is activated (if not, run `\.env\Scripts\activate.bat`)
 - Run `python cli.py <file_path> <github_user> <github_token>` replacing parameters between `<>` as follows: 
 - `file_path`: The path to the YML that should be loaded
 - `github_user`: The Github username for which the project should be deployed
 - `github_token`: The Github personal access token generated through the `Github setup` section 

### API
To host the API:
 - Go to the project root.
 - Make sure that the virtual environment is activated (if not, run `\.env\Scripts\activate.bat`)
 - Set the `FLASK_APP` environment variable by running `set FLASK_APP=flask.py`
 - Start the API's server by running `python -m flask run`

Now that you have the API up and running, make a POST to the `/upload` endpoint. The request must contain a `form-data` payload containing the following keys:
 - `file`: The YML that should be loaded
 - `github_user`: The Github username for which the project should be deployed
 - `github_token`: The Github personal access token generated through the `Github setup` section

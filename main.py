from src.github.deploy import deploy_to_github
from src.jekyll.populate import populate_jekyll

from dotenv import load_dotenv
load_dotenv()

from flask import Flask
app = Flask(__name__)

project_path = './_temp_jekyl_project'

@app.route('/') # type: ignore
def upload_yml():
    populate_jekyll('mock.yml', project_path)
    deploy_to_github(project_path, 'alexpsilva', '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')
    return 'success'
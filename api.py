import os
from src.github.deploy import deploy_to_github
from src.jekyll.populate import populate_jekyll


from dotenv import load_dotenv
load_dotenv()

from flask import Flask, request
app = Flask(__name__)

project_path = './_temp_jekyl_project'
file_upload_path = './_uploads'

if not os.path.isdir(file_upload_path):
    os.mkdir(file_upload_path)

@app.route('/upload', methods=['POST']) # type: ignore
def upload_yml():
    file = list(request.files.values())[0]
    file_path = f'{file_upload_path}/{file.filename}'
    file.save(file_path)

    populate_jekyll(file_path, project_path)

    user = request.form['github_user']
    token = request.form['github_token']
    deploy_to_github(project_path, user, token)
    return f'Deployed to {user}.github.io'
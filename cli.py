import sys
from src.github.deploy import deploy_to_github
from src.jekyll.populate import populate_jekyll

if len(sys.argv) != 4:
    print('Invalid parameters. Please run "python3 cli.py <yml_path> <github_username> <github_token>"')

file_path = sys.argv[1]
user = sys.argv[2]
token = sys.argv[3]

project_path = './_temp_jekyl_project'

populate_jekyll(file_path, project_path)
deploy_to_github(project_path, user, token)
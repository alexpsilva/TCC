import argparse
from src.github.deploy import deploy_to_github
from src.jekyll.populate import populate_jekyll

parser = argparse.ArgumentParser()
parser.add_argument('yml_path', help='Absolute or relative path to the .yml file containing the process description')
parser.add_argument('github_user', help='The Github user that shall host the generated site')
parser.add_argument('github_token', help='The authentication token to the previously defined Github user')

parser.add_argument('-u', '--upload', default=[], nargs='*', help='One or multiple paths to files that should be uploaded and may be referenced throughout the site')

args = parser.parse_args()

project_path = './_temp_jekyl_project'

populate_jekyll(args.yml_path, project_path, args.upload)
deploy_to_github(project_path, args.github_user, args.github_token)
from github.deploy import deploy_to_github
from jekyll.populate import populate_jekyll

project_path = './_temp_jekyl_project'

populate_jekyll('mock.yml', project_path)
deploy_to_github(project_path, 'alexpsilva', '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')
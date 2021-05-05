import GithubAPI

config_path = f'E:/Workspace/jekyl_project_test/_config.yml'

git = GithubAPI('alexpsilva', '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')

with open(config_path, 'r') as file:
    data = file.read()

git.add('_config.yml', data)
git.commit('main', 'Adding config file')
git.push('main')
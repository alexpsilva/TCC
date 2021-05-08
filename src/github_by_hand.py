from github_api import GithubAPI
import os

project_path = f'E:\\Workspace\\jekyl_project_test'
ignore_list = [
    f'{project_path}\\.git',
    f'{project_path}\\.jekyll-cache',
    f'{project_path}\\_site'
]

def should_ignore(path):
    for ignore_path in ignore_list:
        if ignore_path in path:
            return True
    return False

# Scan through the project, fetching files to be commited
dirs_to_walk = [project_path]
files_to_commit = []
while dirs_to_walk:
    root = dirs_to_walk.pop(0)
    for root, dirs, files in os.walk(root):
        for dir in dirs:
            full_path = f'{root}\\{dir}'
            if not should_ignore(full_path):
                dirs_to_walk.append(full_path)
        
        for file in files:
            full_path = f'{root}\\{file}'
            if not should_ignore(full_path):
                files_to_commit.append(full_path)

# Commit and push project files
git = GithubAPI('alexpsilva', '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')
for absolute_path in files_to_commit:
    with open(absolute_path, 'r') as file:
        data = file.read()

    relative_path = absolute_path.replace(project_path + '\\', '')
    print(f'Staging {relative_path} for commit')
    git.add(relative_path, data)

git.commit('main', 'Initial commit (by ASilva)')
git.push('main')
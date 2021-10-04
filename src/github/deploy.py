from .api import GithubAPI
import base64
import os

def deploy_to_github(project_path: str, user: str, token: str) -> None:
    ignore_list = [
        f'{project_path}/.git',
        f'{project_path}/.jekyll-cache',
        f'{project_path}/_site',
        f'{project_path}/_temp_jekyl_project'
    ]

    def should_ignore(path):
        for ignore_path in ignore_list:
            if ignore_path in path:
                return True
        return False
    
    def read_file_contents(path: str) -> bytes:
        with open(path, "rb") as binary_contents:
            return base64.b64encode(binary_contents.read())

    # Scan through the project, fetching files to be commited
    dirs_to_walk = [project_path]
    files_to_commit = set()
    while dirs_to_walk:
        root = dirs_to_walk.pop(0)
        for root, dirs, files in os.walk(root):
            for dir in dirs:
                full_path = f'{root}/{dir}'
                if not should_ignore(full_path):
                    dirs_to_walk.append(full_path)
            
            for file in files:
                full_path = f'{root}/{file}'
                if not should_ignore(full_path):
                    files_to_commit.add(full_path)

    # Commit and push project files
    git = GithubAPI(user, token)
    for absolute_path in files_to_commit:
        try:
            data = read_file_contents(absolute_path)
        except:
            print(f'The file {absolute_path} could not be decoded and, therefore, was not uploaded')
            continue

        relative_path = absolute_path.replace(project_path + '/', '')
        print(f'Staging {relative_path} for commit')
        git.add(relative_path, data)

    print(f'Commiting staged changes')
    git.commit('main')

    print(f'Pushing refs')
    git.push('main')
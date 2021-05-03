import requests
from typing import Callable, Dict, Iterable, Optional, Tuple, Union

from requests.models import HTTPError

JSON = Dict[str, Union[str, int, float, bool, 'JSON', Iterable['JSON']]]

class GITHUB_TREE_FILE_MODES:
    file = '100644'
    executable = '100755'
    subdirectory = '040000'
    submodule = '160000'
    symlink = '120000'

class GithubAPI:
    base_url = 'https://api.github.com'
    base_params: Dict[str, Union[Dict[str, str], Tuple[str, str]]] = {
        'headers': {
            'Accept': 'application/vnd.github.v3+json'
        },
    }

    def __init__(self, user: str, access_token: str) -> None:
        self.base_params['auth'] = (user, access_token)

    def _request(self, endpoint: str, method: Callable, body: Optional[JSON] = None) -> JSON:
        url = self.base_url + endpoint
        params = {'url': url, **self.base_params}
        if body is not None:
            params['json'] = body

        response = method(**params)

        if response.ok:
            return response.json()
        else:
            raise HTTPError

    def get(self, endpoint: str) -> JSON:
        return self._request(endpoint, requests.get)

    def patch(self, endpoint: str, body: JSON) -> JSON:
        return self._request(endpoint, requests.patch, body)

    def put(self, endpoint: str, body: JSON) -> JSON:
        return self._request(endpoint, requests.put, body)

    def post(self, endpoint: str, body: JSON) -> JSON:
        return self._request(endpoint, requests.post, body)

config_path = f'E:/Workspace/jekyl_project_test/_config.yml'

git = GithubAPI('alexpsilva', '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')
user = git.get('/user')['login']

repo = f'{user}.github.io'

try:
    git.get(f'/repos/{user}/{repo}')
except HTTPError:
    git.post('/user/repos', {
        'name': repo,
        'auto_init': True
    })

with open(config_path, 'r') as file:
    data = file.read()

blob = git.post(f'/repos/{user}/{repo}/git/blobs', {
    'owner': user,
    'repo': repo,
    'content': data
})

tree = git.post(f'/repos/{user}/{repo}/git/trees', {
    'owner': user,
    'repo': repo,
    'tree': [{
        'path': '_config.yml', 
        'mode': GITHUB_TREE_FILE_MODES.file, 
        'type': 'blob', 
        'sha': blob['sha']
    }]
})

ref = 'heads/main'
last_ref = git.get(f'/repos/{user}/{repo}/git/refs/{ref}')

commit = git.post(f'/repos/{user}/{repo}/git/commits', {
    'owner': user,
    'repo': repo,
    'message': 'Adding config file',
    'tree': tree['sha'],
    'parents': [last_ref['object']['sha']] # type: ignore
})

new_ref = git.patch(f'/repos/{user}/{repo}/git/refs/{ref}', {
    'owner': user,
    'repo': repo,
    'ref': ref,
    'sha': commit['sha']
})
import requests
from typing import Callable, Dict, Iterable, List, Optional, Set, Tuple, Union

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
    staged_changes: Dict[str, JSON] = {}
    pending_commits: Dict[str, JSON] = {}

    def __init__(self, user: str, access_token: str) -> None:
        self.base_params['auth'] = (user, access_token)
        self.user = self.get('/user')['login']

        self.repo = f'{user}.github.io'

        try:
            self.get(f'/repos/{self.user}/{self.repo}')
        except HTTPError:
            self.post('/user/repos', {
                'name': self.repo,
                'auto_init': True
            })

    def _request(self, endpoint: str, method: Callable, body: Optional[JSON] = None) -> JSON:
        url = self.base_url + endpoint
        params = {'url': url, **self.base_params}
        if body is not None:
            params['json'] = {
                'owner': self.user,
                'repo': self.repo,
                **body
            }

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

    def create_blob(self, content):
        return self.post(
            f'/repos/{self.user}/{self.repo}/git/blobs', 
            { 'content': content }
        )
    
    def create_tree(self, content):
        return self.post(
            f'/repos/{self.user}/{self.repo}/git/trees', 
            { 'tree': content }
        )
    
    def add(self, path, content):
        blob = self.create_blob(content)
        self.staged_changes[path] = blob

    def commit(self, branch, message):
        # Group changes by folder
        get_containing_folder = lambda path: '\\'.join(path.split('\\').pop(-1))
        files_by_folder: Dict[str, List[str]] = {}
        for path in self.staged_changes.keys():
            containing_folder = get_containing_folder(path)
            files_by_folder.setdefault(containing_folder, []).append(path)

        # TO-DO: Create a tree according to the file structure (currently everything goes in the root)

        # Create trees for the staged changes
        blobs = []
        for folder, files in files_by_folder.items():
            for file_path in files:
                blob = self.staged_changes[file_path]
                blobs.append({
                    'path': file_path, 
                    'mode': GITHUB_TREE_FILE_MODES.file, 
                    'type': 'blob', 
                    'sha': blob['sha']
                })

        tree =  self.create_tree(blobs)
        ref = f'heads/{branch}'
        
        # TO-DO: Handle file deletes
        # TO-DO: Handle commits on new branches (without a previous ref)
        # TO-DO: Handle multiple pending commits before pushing changes

        # Commit root tree
        last_ref = self.get(f'/repos/{self.user}/{self.repo}/git/refs/{ref}')
        self.pending_commits[branch] = self.post(
            f'/repos/{self.user}/{self.repo}/git/commits', 
            {
                'message': message,
                'tree': tree['sha'],
                'parents': [last_ref['object']['sha']] # type: ignore
            }
        )
    
    def push(self, branch):
        ref = f'heads/{branch}'
        commit = self.pending_commits[branch]

        return self.patch(
            f'/repos/{self.user}/{self.repo}/git/refs/{ref}',
            { 'ref': ref, 'sha': commit['sha'] }
        )
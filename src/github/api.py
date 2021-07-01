import requests
from typing import Callable, Dict, Optional, Tuple, Union, cast, List
from .types import *

from requests.models import HTTPError

class GithubAPI:
    base_url = 'https://api.github.com'

    def __init__(self, user: str, access_token: str) -> None:
        self.staged_changes = FILE_TREE()
        self.pending_commits: Dict[str, JSON] = {}
        
        self.base_params: Dict[str, Union[Dict[str, str], Tuple[str, str]]] = {
            'headers': {
                'Accept': 'application/vnd.github.v3+json'
            },
            'auth': (user, access_token)
        }
        
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
            raise HTTPError(response.reason)

    def get(self, endpoint: str) -> JSON:
        return self._request(endpoint, requests.get)

    def patch(self, endpoint: str, body: JSON) -> JSON:
        return self._request(endpoint, requests.patch, body)

    def put(self, endpoint: str, body: JSON) -> JSON:
        return self._request(endpoint, requests.put, body)

    def post(self, endpoint: str, body: JSON) -> JSON:
        return self._request(endpoint, requests.post, body)

    def create_blob(self, content: str) -> GithubElement:
        return cast(GithubElement, self.post(
            f'/repos/{self.user}/{self.repo}/git/blobs', 
            { 'content': content }
        ))
    
    def create_tree(self, content: List[Tree]) -> GithubElement:
        return cast(GithubElement, self.post(
            f'/repos/{self.user}/{self.repo}/git/trees', 
            { 'tree': cast(List[JSON], content) }
        ))

    def add(self, path, content):
        blob = self.create_blob(content)
        
        containing_folders = path.split('\\')
        file_name = containing_folders.pop(-1)

        last_folder = self.staged_changes
        for folder in containing_folders:
            last_folder.folders.setdefault(folder, FILE_TREE())
            last_folder = last_folder.folders[folder]
        
        last_folder.files[file_name] = blob

    def _build_tree_from_folder(self, folder: FILE_TREE) -> str:
        contents: List[Tree] = []

        for sub_folder_name, sub_folder in folder.folders.items():
            sub_tree_sha = self._build_tree_from_folder(sub_folder)
            
            contents.append({
                'path': sub_folder_name, 
                'mode': GITHUB_TREE_FILE_MODES.subdirectory, 
                'type': 'tree', 
                'sha': sub_tree_sha
            })

        for file_name, file in folder.files.items():
            contents.append({
                'path': file_name, 
                'mode': GITHUB_TREE_FILE_MODES.file, 
                'type': 'blob', 
                'sha': file['sha']
            })

        tree = self.create_tree(contents)
        return tree['sha']

    def commit(self, branch: str) -> None:
        tree_sha = self._build_tree_from_folder(self.staged_changes)
        
        # TO-DO: Handle commits on new branches (without a previous ref)
        # TO-DO: Handle multiple pending commits before pushing changes

        # Commit root tree
        ref = f'heads/{branch}'
        last_ref = self.get(f'/repos/{self.user}/{self.repo}/git/refs/{ref}')
        last_ref_object = cast(Ref, last_ref['object'])
        last_commit_sha = last_ref_object['sha']

        version = '1.0'
        if last_ref_object['type'] == 'commit':
            last_commit = self.get(f'/repos/{self.user}/{self.repo}/git/commits/{last_commit_sha}')
            try:
                last_version = last_commit['message'].replace('Version ', '') # type: ignore
                version = '{:1.1f}'.format(float(last_version) + 0.1)
            except:
                pass

        self.pending_commits[branch] = self.post(
            f'/repos/{self.user}/{self.repo}/git/commits', 
            {
                'message': f'Version {version}',
                'tree': tree_sha,
                'parents': [last_commit_sha]
            }
        )
    
    def push(self, branch):
        ref = f'heads/{branch}'
        commit = self.pending_commits[branch]

        return self.patch(
            f'/repos/{self.user}/{self.repo}/git/refs/{ref}',
            { 'ref': ref, 'sha': commit['sha'] }
        )
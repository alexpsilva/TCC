from typing import Dict, Iterable, Union
from typing_extensions import Literal, TypedDict

class GITHUB_TREE_FILE_MODES:
    file = '100644'
    executable = '100755'
    subdirectory = '040000'
    submodule = '160000'
    symlink = '120000'

class GithubElement(TypedDict):
    sha: str
    url: str

GITHUB_TREE_TYPES = Literal['blob', 'tree', 'commit']

class Tree(TypedDict):
    path: str 
    mode: str # Ideally, restrict to a member of GITHUB_TREE_FILE_MODES
    type: GITHUB_TREE_TYPES
    sha: str

JSON_ELEMENT = Union[str, int, float, bool, 'JSON', Iterable['JSON_ELEMENT']]
JSON = Dict[str, JSON_ELEMENT]

class FILE_TREE:
    def __init__(self):
        self.files: Dict[str, GithubElement] = {}
        self.folders: Dict[str, 'FILE_TREE'] = {}
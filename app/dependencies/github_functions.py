import requests, base64
from semantic_version import SimpleSpec
from github_release_downloader import check_and_download_updates, GitHubRepo
from pathlib import Path

import re
class GithubActions():
    '''a class to manage github actions like downloading files 
    from release pages and other associated internet actions'''

    def __init__(self,
        owner:str,
        repo:str,
        token:str,
        dest:str):
        pass

    def set_dest(self, destination:str):
        self.dest = destination

    def download_windows(self):
        check_and_download_updates(
                GitHubRepo(self.owner, self.repo, self.token),  # Releases source
                SimpleSpec("~1.1"),  # Search 1.1.0 compatible version
                assets_mask=re.compile(".*\\.exe"),  # Download *.exe only
                downloads_dir=Path(self.dest),  # Where to download
            )
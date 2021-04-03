import subprocess

import git

from settings import REPOSITORIES, dir_file
from utils import make_error


class Clone:
    def __init__(self, name):
        self.name = name
        self.address = REPOSITORIES.get(name)
        self.actions = ['install', 'build']
        self.errors = None
        self.clone_repo()
        self.build()

    def clone_repo(self):
        if self.address:
            try:
                git.Git(f"{dir_file}").clone(self.address)
            except git.GitCommandError as e:
                self.errors = make_error(400, 'Problems with the specified GIT repository', e.stderr)
        else:
            self.errors = make_error(400, 'Incorrect repo selected ', '')

    def build(self):
        if not self.errors:
            for a in self.actions:
                action = subprocess.run(
                    f"npm {a}",
                    shell=True,
                    cwd=f'{dir_file}/{self.name}',
                    capture_output=True,
                    text=True,
                    timeout=60)
                if action.returncode != 0:
                    self.errors = make_error(500, f'Npm {a} error', action.stderr)
                    break

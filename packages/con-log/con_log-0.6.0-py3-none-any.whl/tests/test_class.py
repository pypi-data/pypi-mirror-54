

import pytest

from conlog import Conlog

def is_other_user(user):
    console = Conlog.get_console('main')
    console.debug(r"~ {user}=")
    return True

class Env:
    def __init__(self):
        # Importing functions
        pass

    def get_shell(self):
        console = Conlog.get_console('main')
        console.log('it works')
        is_other_user()
        return "shell"

def test_all_instance():
    env_map = Env()
    env_map.get_shell()

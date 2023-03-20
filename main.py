import os
from collections.abc import Iterable

from colorama import init as initcolorama

import resources.utils.CLI as cli

if __name__ == "__main__":
    initcolorama()

    folders = ['ghosts', 'saves', 'miis']
    for folder in folders:
        if not os.path.exists(folder):
            os.mkdir(folder)

    cli.clear()
    sm = cli.StateManager()
    while True:
        if isinstance(sm.args, Iterable):
            sm.active(sm, *sm.args)
        else:
            sm.active(sm, sm.args)

import os
import sys
from collections.abc import Iterable

from colorama import init as initcolorama

import resources.utils.CLI as cli

if __name__ == "__main__":
    initcolorama()

    if getattr(sys, 'frozen', False):  # checks if executable from pyinstaller
        app_path = os.path.dirname(sys.executable)
    else:
        app_path = os.path.dirname(os.path.abspath(__file__))

    os.chdir(app_path)

    # folders = ['ghosts', 'saves', 'miis']
    folders = ['ghosts']
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

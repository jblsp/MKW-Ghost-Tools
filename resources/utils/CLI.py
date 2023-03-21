import os
import sys
if os.name == "nt":
    import msvcrt
if os.name == "posix":
    import tty
    import termios

from colorama import Fore

import resources.utils.functions as func
from resources.utils.ghost import Ghost
from states import initial


class StateManager:
    def __init__(self):
        self.active = initial
        self.args = ()
        self.tree = []

    def switch(self, new_state, args=(), error_msg: str = "", feedback_msg: str = ""):
        clear()
        if error_msg:
            print(Fore.RED + error_msg + Fore.RESET)
        if feedback_msg:
            print(Fore.GREEN + feedback_msg + Fore.RESET)

        if new_state == "back":
            new_state, args = self.tree.pop()
        elif new_state != self.active:
            self.tree.append((self.active, self.args))

        self.active = new_state
        self.args = args


def clear():
    if os.name == 'nt':
        os.system('cls')
    if os.name == 'posix':
        os.system('clear')
    print(title + "\n" + Fore.RESET)


def getch():
    if os.name == 'nt':
        return msvcrt.getch().decode('utf-8')
    if os.name == 'posix':
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            char = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return char


def exit():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')
    os._exit(0)


def choice(state, choices: dict = None, prompt: str = "") -> str:
    back = False
    if state.tree:
        back = True
    if prompt:
        print(Fore.LIGHTWHITE_EX + prompt + Fore.RESET)
    choices_list = []
    options_length = len(choices)
    keys = tuple(choices.keys())
    values = tuple(choices.values())
    for i in range(options_length):
        choices_list.append(f"[{keys[i]}] {values[i]}")
    if back:
        choices_list.append("[b] Back")
    choices_list.append(Fore.RED + "[x] Exit" + Fore.RESET)
    print('\n'.join(choices_list))
    selection = getch().lower()
    clear()
    if selection == "x":
        exit()
    if selection == "b" and back:
        state.switch("back")
    return selection


def select_ghost(state) -> Ghost:
    ghosts = func.get_ghosts()
    if not ghosts:
        state.switch("back", error_msg="There are no ghost files in /ghosts")
    print("[r] Refresh list".ljust(40) + '[b] Back')
    lines = []
    column2_index = 0
    for i, ghost in enumerate(ghosts):
        str_ = f"[{i + 1}] {func.preview_ghost(ghost)}"
        if i <= len(ghosts) // 2:
            lines.append(str_.ljust(40))
        else:
            lines[column2_index] += str_
            column2_index += 1
    lines.append(''.ljust(40))
    lines[-1] += Fore.RED + '[x] Exit' + Fore.RESET
    print('\n'.join(lines))
    selection = input(Fore.LIGHTYELLOW_EX + '\nEnter a ghost or option: ' + Fore.RESET)
    clear()
    if selection == 'r':
        pass
    elif selection == 'x':
        exit()
    elif selection == 'b':
        state.switch("back")
    else:
        try:
            return ghosts[int(selection) - 1]
        except (IndexError, ValueError):
            print(Fore.RED + "Enter a valid index." + Fore.RESET)


def create_title():
    mkw = [
        " __  __  _  __ _    _  ",
        "|  \/  || |/ /| |  | | ",
        "| \  / || | / | |/\| | ",
        "| |\/| || | \ |  /\  | ",
        "|_|  |_||_|\_\|_|  |_| ", ]

    ghost = (
        "   ________               __  ",
        "  / ____/ /_  ____  _____/ /_ ",
        " / / __/ __ \/ __ \/ ___/ __/ ",
        "/ /_/ / / / / /_/ /__  / /_   ",
        "\____/_/ /_/\____/____/\__/   ",)

    tool = (
        "  ______            __    ",
        " /_  __/___  ____  / /____",
        "  / / / __ \/ __ \/ / ___/",
        " / / / /_/ / /_/ / /__  ) ",
        "/_/  \____/\____/_/____/  ",)

    mkw_color = Fore.BLUE
    ghost_color = Fore.LIGHTWHITE_EX
    editor_color = Fore.LIGHTWHITE_EX

    title_ = []
    for i in range(len(mkw)):
        title_.append(mkw_color + mkw[i] + ghost_color + ghost[i] + editor_color + tool[i])
    return "\n".join(title_)


title = create_title()

import resources.utils.CLI as cli
import resources.utils.functions as func
from resources.utils.ghost import Ghost


def initial(state):
    selection = cli.choice(state, prompt="What would you like to do?", choices={
        "g": "Ghost Manager",
        # "s": "Save Manager",
        # "m": "Mii Manager",
        # "t": "Create top 10 (by WhatisLoaf)",
        # "i": "Generate input viewer (by WhatisLoaf)",
    })
    if selection == "g":
        state.switch(ghost_manager)
    if selection == "s":
        pass
    if selection == "t":
        pass
    if selection == "i":
        pass


def ghost_manager(state):
    selection = cli.choice(state, prompt="Select an option:", choices={
        "o": "Open Ghost",
        "t": "Tools"
    })
    if selection == "o":
        state.switch(open_ghost)
    if selection == "t":
        state.switch(ghost_tools)


def open_ghost(state):
    ghost = cli.select_ghost(state)
    if isinstance(ghost, Ghost):
        state.switch(selected_ghost, args=ghost)


def selected_ghost(state, ghost):
    ghost_view_col1 = [
        f"Track: {ghost.get_track_name()}",
        "",
        f"Time: {ghost.get_time()}",
        f"Lap 1: {ghost.get_lap(1)}",
        f"Lap 2: {ghost.get_lap(2)}",
        f"Lap 3: {ghost.get_lap(3)}",
        "",
        f"Ghost Type: {ghost.get_ghost_type()}",
        f"Compression: {ghost.get_compression()}"
    ]
    ghost_view_col2 = [
        f"Mii Name: {ghost.get_mii_name()}",
        f"Country: {ghost.get_country()}",
        f"Controller: {ghost.get_controller()}",
        "",
        f"Character: {ghost.get_character()}",
        f"Vehicle: {ghost.get_vehicle()}",
        f"Drift Type: {ghost.get_drift_type()}",
        "",
        f"Date Set: {ghost.get_date_set()}"
    ]

    ghost_view = []
    for i in range(len(ghost_view_col1)):
        try:
            col1 = ghost_view_col1[i].ljust(40)
        except IndexError:
            col1 = "".ljust(40)
        try:
            col2 = ghost_view_col2[i]
        except IndexError:
            col2 = "".ljust(40)
        ghost_view.append(col1 + col2)

    print('\n'.join(ghost_view) + '\n')

    selection = cli.choice(state, choices={
        # "e": "Edit values",
        # "r": "Rename file",
        # "d": "Delete file",
    })


def ghost_tools(state):
    selection = cli.choice(state, prompt="Ghost Tools", choices={
        "f": "Format ghost filenames"
    })
    if selection == 'f':
        ghosts = func.get_ghosts()
        for ghost in ghosts:
            func.format_ghost_fname(ghost)
        state.switch(ghost_tools, feedback_msg="Ghost names formatted")

import os
from hashlib import sha256

from resources.utils.ghost import Ghost


def get_ghosts() -> list:
    ghosts = []
    for i, fname in enumerate(os.listdir('ghosts')):
        if fname.endswith('.rkg'):
            new_ghost = Ghost(fname)
            if new_ghost.identifier == b'RKGD':
                ghosts.append(new_ghost)
    return ghosts


def format_ghost_fname(ghost: Ghost):
    year = str(ghost.data['year'] + 2000).zfill(4)
    month = str(ghost.data['month']).zfill(2)
    day = str(ghost.data['day']).zfill(2)
    lap1 = f"{str(ghost.data['lap1_seconds'] + 60 * ghost.data['lap1_minutes'])}.{str(ghost.data['lap1_milliseconds']).zfill(3)}"
    lap2 = f"{str(ghost.data['lap2_seconds'] + 60 * ghost.data['lap1_minutes'])}.{str(ghost.data['lap2_milliseconds']).zfill(3)}"
    lap3 = f"{str(ghost.data['lap3_seconds'] + 60 * ghost.data['lap1_minutes'])}.{str(ghost.data['lap3_milliseconds']).zfill(3)}"
    date_laps = bytes(f"{year} {month} {day} {lap1} {lap2} {lap3}", 'utf-16')
    hash_ = sha256(date_laps)
    # to avoid issues where ghosts with the same mii name/track tie
    ghost_id = hash_.hexdigest()[:4]
    new_fname = f"{track_abbrev(ghost.get_track_name())}_{ghost.get_time().replace(':', '-')}_{ghost.get_mii_name()}_{ghost_id}.rkg"
    os.rename(f'ghosts/{ghost.fname}', f'ghosts/{new_fname}')
    ghost.fname = new_fname


def track_abbrev(track_name) -> str:
    list_ = track_name.split(' ')
    for i, str_ in enumerate(list_):
        all_upper = True
        for char in str_:
            if char.islower():
                all_upper = False
        if str_ in ('SNES', 'N64', 'GBA', 'DS', 'GCN'):
            list_[i] = 'r'
        elif not all_upper:
            list_[i] = str_[0]
    return ''.join(list_)


def preview_ghost(ghost: Ghost) -> str:
    return f"{track_abbrev(ghost.get_track_name())} - {ghost.get_time()} - {ghost.get_mii_name()}"

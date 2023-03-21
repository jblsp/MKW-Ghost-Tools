class Ghost:
    def __init__(self, fname: str):

        with open(f"ghosts/{fname}", "rb") as f:
            bytes_ = f.read(0x86)
            binary = ''.join([bin(byte).replace('0b', '').zfill(8)
                             for byte in bytes_])

        def read_bits(mem_offset: hex, starting_location: int, bits: int) -> int:
            start = 8*mem_offset+starting_location
            if bits == 1:
                return int(binary[start])
            return int(binary[start:start+bits], 2)

        self.fname = fname
        self.identifier = bytes_[:0x04]

        self.data = {
            "minutes": read_bits(*mem_locations["minutes"]),
            "seconds": read_bits(*mem_locations["seconds"]),
            "milliseconds": read_bits(*mem_locations["milliseconds"]),
            "track_id": read_bits(*mem_locations["track_id"]),
            "vehicle_id": read_bits(*mem_locations["vehicle_id"]),
            "character_id": read_bits(*mem_locations["character_id"]),
            "year": read_bits(*mem_locations["year"]),
            "month": read_bits(*mem_locations["month"]),
            "day": read_bits(*mem_locations["day"]),
            "controller_id": read_bits(*mem_locations["controller_id"]),
            "compression": read_bits(*mem_locations["compression"]),
            "ghost_type": read_bits(*mem_locations["ghost_type"]),
            "drift_type": read_bits(*mem_locations["drift_type"]),
            "lap_count": read_bits(*mem_locations["lap_count"]),
            "lap1_minutes": read_bits(*mem_locations["lap1_minutes"]),
            "lap1_seconds": read_bits(*mem_locations["lap1_seconds"]),
            "lap1_milliseconds": read_bits(*mem_locations["lap1_milliseconds"]),
            "lap2_minutes": read_bits(*mem_locations["lap2_minutes"]),
            "lap2_seconds": read_bits(*mem_locations["lap2_seconds"]),
            "lap2_milliseconds": read_bits(*mem_locations["lap2_milliseconds"]),
            "lap3_minutes": read_bits(*mem_locations["lap3_minutes"]),
            "lap3_seconds": read_bits(*mem_locations["lap3_seconds"]),
            "lap3_milliseconds": read_bits(*mem_locations["lap3_milliseconds"]),
            "country_code": read_bits(*mem_locations["country_code"]),
            "state_code": read_bits(*mem_locations["state_code"]),
            "location_code": read_bits(*mem_locations["location_code"]),
        }

        self.mii_data = bytes_[0x3C:0x3C+0x4A]

    def get_mii_name(self) -> str:
        return self.mii_data[0x2:0x15+1].decode("utf-16be").replace('\x00', '')

    def get_time(self) -> str:
        if self.data['minutes']:
            return f"{self.data['minutes']}:{str(self.data['seconds']).zfill(2)}.{str(self.data['milliseconds']).zfill(3)}"
        else:
            return f"{str(self.data['seconds']).zfill(2)}.{str(self.data['milliseconds']).zfill(3)}"

    def get_lap(self, lap: int) -> str:
        ms = str(self.data[f'lap{lap}_milliseconds']).zfill(3)
        if self.data[f'lap{lap}_minutes']:
            return f"{self.data[f'lap{lap}_minutes']}:{str(self.data[f'lap{lap}_seconds']).zfill(2)}.{ms}"
        else:
            return f"{self.data[f'lap{lap}_seconds']}.{ms}"

    def get_ghost_type(self) -> str:
        return ghost_type[self.data['ghost_type']]

    def get_track_name(self) -> str:
        return track_ids[self.data['track_id']]

    def get_compression(self) -> str:
        return {
            0: "Raw",
            1: "YAZ1"
        }[self.data['compression']]

    def get_country(self) -> str:
        return country[self.data['country_code']]

    def get_controller(self) -> str:
        return {
            0: "Wii Wheel",
            1: "Wiimote + Nunchuk",
            2: "Classic",
            3: "GameCube"
        }[self.data['controller_id']]

    def get_character(self) -> str:
        return character_ids[self.data['character_id']]

    def get_vehicle(self) -> str:
        return vehicle_ids[self.data['vehicle_id']]

    def get_drift_type(self) -> str:
        return {
            0: "Manual",
            1: "Automatic"
        }[self.data['drift_type']]

    def get_date_set(self) -> str:
        months = {
            1: "Jan",
            2: "Feb",
            3: "Mar",
            4: "Apr",
            5: "May",
            6: "Jun",
            7: "Jul",
            8: "Aug",
            9: "Sep",
            10: "Oct",
            11: "Nov",
            12: "Dec"
        }
        return f"{months[self.data['month']]} {self.data['day']} {self.data['year'] + 2000}"

    def write_to_file(self):
        with open(f"ghosts/{self.fname}", "rb") as f:
            bytes_ = f.read()
            binary = ''.join([bin(byte).replace('0b', '').zfill(8)
                             for byte in bytes_])

        def write_bits(mem_offset: hex, starting_location: int, bits: int, write: int) -> int:
            nonlocal binary
            start = 8*mem_offset+starting_location
            if bits == 1:
                binary = binary[:start] + str(write) + binary[start+1:]
            else:
                binary = binary[:start] + str(bin(write)).replace(
                    '0b', '').zfill(bits) + binary[start+bits+1:]

        for item in self.data.keys():
            write_bits(*mem_locations[item], self.data[item])

        bytes_ = bytearray([int(binary[i:i+8], 2)
                           for i in range(0, len(binary), 8)])
        bytes_[0x3C:0x3C+0x4A] = self.mii_data
        with open(f"ghosts/{self.fname}", "wb") as f:
            f.write(bytes_)


mem_locations = {  # (mem_offset, starting_location, bits)
    "minutes": (0x04, 0, 7),
    "seconds": (0x04, 7, 7),
    "milliseconds": (0x05, 6, 10),
    "track_id": (0x07, 0, 6),
    "vehicle_id": (0x08, 0, 6),
    "character_id": (0x08, 6, 6),
    "year": (0x09, 4, 7),
    "month": (0x0A, 3, 4),
    "day": (0x0A, 7, 5),
    "controller_id": (0x0B, 4, 4),
    "compression": (0x0C, 4, 1),
    "ghost_type": (0x0C, 7, 7),
    "drift_type": (0x0D, 6, 1),
    "lap_count": (0x10, 0, 8),
    "lap1_minutes": (0x11, 0, 7),
    "lap1_seconds": (0x11, 7, 7),
    "lap1_milliseconds": (0x11, 14, 10),
    "lap2_minutes": (0x11, 24, 7),
    "lap2_seconds": (0x11, 31, 7),
    "lap2_milliseconds": (0x11, 38, 10),
    "lap3_minutes": (0x11, 48, 7),
    "lap3_seconds": (0x11, 55, 7),
    "lap3_milliseconds": (0x11, 62, 10),
    "country_code": (0x34, 0, 8),
    "state_code": (0x35, 0, 8),
    "location_code": (0x36, 0, 16),
}

track_ids = {
    8: "Luigi Circuit",
    1: "Moo Moo Meadows",
    2: "Mushroom Gorge",
    4: "Toad's Factory",
    0: "Mario Cricuit",
    5: "Coconut Mall",
    6: "DK Summit",
    7: "Wario's Gold Mine",
    9: "Daisy Circuit",
    15: "Koopa Cape",
    11: "Maple Treeway",
    3: "Grumble Volcano",
    14: "Dry Dry Ruins",
    10: "Moonview Highway",
    12: "Bowser's Castle",
    13: "Rainbow Road",
    16: "GCN Peach Beach",
    20: "DS Yoshi Falls",
    25: "SNES Ghost Valley 2",
    26: "N64 Mario Raceway",
    27: "N64 Sherbet Land",
    31: "GBA Shy Guy Beach",
    23: "DS Delfino Square",
    18: "GCN Waluigi Stadium",
    21: "DS Desert Hills",
    30: "GBA Bowser Castle 3",
    29: "N64 DK's Jungle Parkway",
    17: "GCN Mario Circuit",
    24: "SNES Mario Circuit 3",
    22: "DS Peach Gardens",
    19: "GCN DK Mountain",
    28: "N64 Bowser's Castle"
}

character_ids = {
    0: "Mario",
    1: "Baby Peach",
    2: "Waluigi",
    3: "Bowser",
    4: "Baby Daisy",
    5: "Dry Bones",
    6: "Baby Mario",
    7: "Luigi",
    8: "Toad",
    9: "Donkey Kong",
    10: "Yoshi",
    11: "Wario",
    12: "Baby Luigi",
    13: "Toadette",
    14: "Koopa Troopa",
    15: "Daisy",
    16: "Peach",
    17: "Birdo",
    18: "Diddy Kong",
    19: "King Boo",
    20: "Bowser Jr.",
    21: "Dry Bowser",
    22: "Funky Kong",
    23: "Rosalina",
    24: "Small Mii Outfit A (Male)",
    25: "Small Mii Outfit A (Female)",
    26: "Small Mii Outfit B (Male)",
    27: "Small Mii Outfit B (Female)",
    28: "Small Mii Outfit C (Male)",
    29: "Small Mii Outfit C (Female)",
    30: "Medium Mii Outfit A (Male)",
    31: "Medium Mii Outfit A (Female)",
    32: "Medium Mii Outfit B (Male)",
    33: "Medium Mii Outfit B (Female)",
    34: "Medium Mii Outfit C (Male)",
    35: "Medium Mii Outfit C (Female)",
    36: "Large Mii Outfit A (Male)",
    37: "Large Mii Outfit A (Female)",
    38: "Large Mii Outfit B (Male)",
    39: "Large Mii Outfit B (Female)",
    40: "Large Mii Outfit C (Male)",
    41: "Large Mii Outfit C (Female)",
    42: "Medium Mii",
    43: "Small Mii",
    44: "Large Mii",
    45: "Peach Biker Outfit",
    46: "Daisy Biker Outfit",
    47: "Rosalina Biker Outfit"
}

vehicle_ids = {
    0: "Standard Kart S",
    1: "Standard Kart M",
    2: "Standard Kart L",
    3: "Booster Seat",
    4: "Classic Dragster",
    5: "Offroader",
    6: "Mini Beast",
    7: "Wild Wing",
    8: "Flame Flyer",
    9: "Cheep Charger",
    10: "Super Blooper",
    11: "Piranha Prowler",
    12: "Tiny Titan",
    13: "Daytripper",
    14: "Jetsetter",
    15: "Blue Falcon",
    16: "Sprinter",
    17: "Honeycoupe",
    18: "Standard Bike S",
    19: "Standard Bike M",
    20: "Standard Bike L",
    21: "Bullet Bike",
    22: "Mach Bike",
    23: "Flame Runner",
    24: "Bit Bike",
    25: "Sugar Scoot",
    26: "Wario Bike",
    27: "Quacker",
    28: "Zip Zip",
    29: "Shooting Star",
    30: "Magikruser",
    31: "Sneakster",
    32: "Spear",
    33: "Jet Bubble",
    34: "Dolphin Dasher",
    35: "Phantom"
}

ghost_type = {
    1: "Player's Best Time",
    2: "World Record Ghost",
    3: "Continental Record Ghost",
    4: "Flag Challenge Ghost",
    6: "Ghost Race",
    7: "Friend Ghost 01",
    8: "Friend Ghost 02",
    9: "Friend Ghost 03",
    10: "Friend Ghost 04",
    11: "Friend Ghost 05",
    12: "Friend Ghost 06",
    13: "Friend Ghost 07",
    14: "Friend Ghost 08",
    15: "Friend Ghost 09",
    16: "Friend Ghost 10",
    17: "Friend Ghost 11",
    18: "Friend Ghost 12",
    19: "Friend Ghost 13",
    20: "Friend Ghost 14",
    21: "Friend Ghost 15",
    22: "Friend Ghost 16",
    23: "Friend Ghost 17",
    24: "Friend Ghost 18",
    25: "Friend Ghost 19",
    26: "Friend Ghost 20",
    27: "Friend Ghost 21",
    28: "Friend Ghost 22",
    29: "Friend Ghost 23",
    30: "Friend Ghost 24",
    31: "Friend Ghost 25",
    32: "Friend Ghost 26",
    33: "Friend Ghost 27",
    34: "Friend Ghost 28",
    35: "Friend Ghost 29",
    36: "Friend Ghost 30",
    37: "Normal Staff Ghost",
    38: "Expert Staff Ghost",
}

country = {
    1: "Japan",
    8: "Anguilla",
    9: "Antigua and Barbuda",
    10: "Argentina",
    11: "Aruba",
    12: "Bahamas",
    13: "Barbados",
    14: "Belize",
    15: "Bolivia",
    16: "Brazil",
    17: "British Virgin Islands",
    18: "Canada",
    19: "Cayman Islands",
    20: "Chile",
    21: "Colombia",
    22: "Costa Rica",
    23: "Dominica",
    24: "Dominican Republic",
    25: "Ecuador",
    26: "El Salvador",
    27: "French Guiana",
    28: "Grenada",
    29: "Guadeloupe",
    30: "Guatemala",
    31: "Guyana",
    32: "Haiti",
    33: "Honduras",
    34: "Jamaica",
    35: "Martinique",
    36: "Mexico",
    37: "Montserrat",
    38: "Netherlands Antilles",
    39: "Nicaragua",
    40: "Panama",
    41: "Paraguay",
    42: "Peru",
    43: "St. Kitts and Nevis",
    44: "St. Lucia",
    45: "St. Vincent and the Grenadines",
    46: "Suriname",
    47: "Trinidad and Tobago",
    48: "Turks and Caicos Islands",
    49: "United States",
    50: "Uruguay",
    51: "US Virgin Islands",
    52: "Venezuela",
    64: "Albania",
    65: "Australia",
    66: "Austria",
    67: "Belgium",
    68: "Bosnia and Herzegovina",
    69: "Botswana",
    70: "Bulgaria",
    71: "Croatia",
    72: "Cyprus",
    73: "Czech Republic",
    74: "Denmark",
    75: "Estonia",
    76: "Finland",
    77: "France",
    78: "Germany",
    79: "Greece",
    80: "Hungary",
    81: "Iceland",
    82: "Ireland",
    83: "Italy",
    84: "Latvia",
    85: "Lesotho",
    86: "Lichtenstein",
    87: "Lithuania",
    88: "Luxembourg",
    89: "F.Y.R of Macedonia",
    90: "Malta",
    91: "Montenegro",
    92: "Mozambique",
    93: "Namibia",
    94: "Netherlands",
    95: "New Zealand",
    96: "Norway",
    97: "Poland",
    98: "Portugal",
    99: "Romania",
    100: "Russia",
    101: "Serbia",
    102: "Slovakia",
    103: "Slovenia",
    104: "South Africa",
    105: "Spain",
    106: "Swaziland",
    107: "Sweden",
    108: "Switzerland",
    109: "Turkey",
    110: "United Kingdom",
    111: "Zambia",
    112: "Zimbabwe",
    113: "Azerbaijan",
    114: "Mauritania (Islamic Republic of Mauritania)",
    115: "Mali (Republic of Mali)",
    116: "Niger (Republic of Niger)",
    117: "Chad (Republic of Chad)",
    118: "Sudan (Republic of the Sudan)",
    119: "Eritrea (State of Eritrea)",
    120: "Djibouti (Republic of Djibouti)",
    121: "Somalia (Somali Republic)",
    128: "Taiwan",
    136: "South Korea",
    144: "Hong Kong",
    145: "Macao",
    152: "Indonesia",
    153: "Singapore",
    154: "Thailand",
    155: "Philippines",
    156: "Malaysia",
    160: "China",
    168: "U.A.E.",
    169: "India",
    170: "Egypt",
    171: "Oman",
    172: "Qatar",
    173: "Kuwait",
    174: "Saudi Arabia",
    175: "Syria",
    176: "Bahrain",
    177: "Jordan",
}

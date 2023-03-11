import resources.utils.functions as cli
import resources.ids.mkw_ids as mkwids


class Ghost:
    def __init__(self, fname: str):

        with open(f"ghosts/{fname}", "rb") as f:
            bytes_ = f.read(0x86)
            binary = ''.join([bin(byte).replace('0b', '').zfill(8) for byte in bytes_])

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

    def preview(self) -> str:  # should be moved to utils.py
        return f"{cli.track_abbrev(self.get_track_name())} - {self.get_time()} - {self.get_mii_name()}"

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
        return mkwids.ghost_type[self.data['ghost_type']]
    
    def get_track_name(self) -> str:
        return mkwids.track_ids[self.data['track_id']]
    
    def get_compression(self) -> str:
        return mkwids.compression[self.data['compression']]
    
    def write_to_file(self):
        with open(f"ghosts/{self.fname}", "rb") as f:
            bytes_ = f.read()
            binary = ''.join([bin(byte).replace('0b','').zfill(8) for byte in bytes_])

        def write_bits(mem_offset: hex, starting_location: int, bits: int, write: int) -> int:
            nonlocal binary
            start = 8*mem_offset+starting_location
            if bits == 1:
                binary = binary[:start] + str(write) + binary[start+1:]
            else:
                binary = binary[:start] + str(bin(write)).replace('0b','').zfill(bits) + binary[start+bits+1:]

        for item in self.data.keys():
            write_bits(*mem_locations[item], self.data[item])

        bytes_ = bytearray([int(binary[i:i+8], 2) for i in range(0, len(binary), 8)])
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

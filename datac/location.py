from dataclasses import dataclass

@dataclass
class Location:
    """ location data """
    location_id: int
    location_name: str
    country_code: str
    lon: float
    lat: float
    matchme: str
    state_code:str = "" 

    def __init__(self, location_id: int, location_name:str, country_code: str, state_code: str, lon:float, lat: float):
        self.location_id = location_id
        self.location_name = location_name
        self.country_code = country_code
        self.state_code = state_code
        self.lon = lon
        self.lat = lat
        self.matchme = (location_name + country_code).strip() + ((" " + state_code) if state_code != "" else "")

#weather data
from dataclasses import dataclass

@dataclass
class Weather:
    location_id: int
    """ unix timestamp """
    recorded_date: int
    weather_type: int
    temperature_id: int
    precipitation_id: int | None
    wind_id: int
    day_loc_id: int
    clouds_percent: float
    visibility: float

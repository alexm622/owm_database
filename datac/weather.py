#weather data
from dataclasses import dataclass
from datetime import datetime

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
    tup: tuple

    def __init__(self, location_id: int, recorded_date: int, weather_type: int, temperature_id: int, precipitation_id: int | None, wind_id: int, day_loc_id: int, clouds_percent: float, visibility: float) -> None:
        self.location_id = location_id
        self.recorded_date = recorded_date
        self.weather_type = weather_type
        self.temperature_id = temperature_id
        self.precipitation_id = precipitation_id
        self.wind_id = wind_id
        self.day_loc_id = day_loc_id
        self.clouds_percent = clouds_percent
        self.visibility = visibility

        self.tup = (location_id,datetime.fromtimestamp(recorded_date).strftime('%Y-%m-%d %H:%M:%S') ,weather_type, temperature_id, precipitation_id, wind_id, day_loc_id, clouds_percent, visibility)

#data mapper

from datac.location import Location
from datac.weather import Weather

import database_integration.push_data as pd


def loc_to_datac(tup: tuple) -> Location:
    assert(len(tup) is 6)
    return Location(tup[0],tup[1],tup[2],tup[3],tup[4],tup[5])

def json_data(json: dict, location_id: int) -> Weather:
    recorded_date = json.get("dt")
    assert(recorded_date is not None)
    w_type = json.get("weather")
    assert(w_type is not None)
    weather_type = pd.get_weather_type(w_type[0])
    temperature_id = pd.get_temp_id(json.get("main"), location_id, recorded_date)
    wind_id = pd.get_wind_id(json.get("wind"), location_id, recorded_date)
    visibility = json.get("visibility")
    clouds = json.get("clouds")
    assert(clouds is not None)
    clouds = clouds.get("all")
    assert(clouds is not None)
    precipitation_id: int | None
    if(json.get("rain") is None and json.get("snow") is None):
        precipitation_id = None
    else:
        snow = False
        precip = json.get("rain")
        if(precip is None):
            precip = json.get("snow")
            snow = True
            assert(precip is not None)
        precipitation_id = pd.get_precipitation_id(precip, location_id, snow, recorded_date)
    timezone = json.get("timezone")
    assert(timezone is not None)
    day_loc_data = pd.get_day_loc(json.get("sys"), location_id, int(timezone))
    assert(visibility is not None)
    weather = Weather(location_id, recorded_date, weather_type, temperature_id, precipitation_id, wind_id, day_loc_data, 
                      clouds, visibility)
    pd.mydb.commit()

    return weather



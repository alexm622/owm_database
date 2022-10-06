#data mapper

from datac.location import Location
from datac.weather import Weather


def loc_to_datac(tup: tuple) -> Location:
    assert(len(tup) is 6)
    return Location(tup[0],tup[1],tup[2],tup[3],tup[4],tup[5])

def json_data(json: dict, location_id: int) -> Weather:
    weather_type = get_weather_type(json.get("weather"))
    temperature_id = get_temp_id(json.get("main"))
    wind_id = get_wind_id(json.get("wind"))
    visibility = json.get("visibility")
    clouds = json.get("clouds")
    assert(clouds is not None and clouds is dict)
    clouds = clouds.get("all")
    assert(clouds is not None)
    precipitation_id: int | None
    if(json.get("rain") is not None and json.get("snow") is not None):
        print("no precipitation")
        precipitation_id = None
    else:
        precip = json.get("rain")

        if(precip is None):
            precip = json.get("snow")
            assert(precip is not None)
        precipitation_id = get_precipitation_id(precip)
    day_loc_data = get_day_loc(json.get("sys"))
    recorded_date = json.get("dt")
    assert(recorded_date is not None)
    assert(visibility is not None)
    weather = Weather(location_id, recorded_date, weather_type, temperature_id, precipitation_id, wind_id, day_loc_data, 
                      clouds, visibility)

    return weather



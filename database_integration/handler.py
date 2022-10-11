#handler functions

from database_integration.push_data import get_locations, push
from datac.location import Location
import datac.mapper as m
from datac.weather import Weather


def json_to_locations(data: dict) -> list[tuple[Location, dict]]:
    out: list[tuple[Location, dict]] = []
    locs = get_locations()
    for l in locs:
        l_dict = data.get(l.matchme)
        assert(l_dict is not None)
        out.append((l, l_dict))
    return out

def json_to_weather(data: dict):
    locs = json_to_locations(data)
    for t in locs:
        id = t[0].location_id
        w:Weather = m.json_data(t[1],id)
        push(w)

    
    

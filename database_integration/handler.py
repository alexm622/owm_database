#handler functions

from database_integration.push_data import get_locations, push
from datac.location import Location
import datac.mapper as m
from datac.weather import Weather


def json_to_locations(data: dict) -> list[tuple[Location, dict]]:
    out: list[tuple[Location, dict]] = []
    locs = get_locations()
    print("locs ", locs)
    print("keys: ", data.keys())
    for l in locs:
        print("matchme: ", l.matchme)
        l_dict = data.get(l.matchme)
        print("l_dict: ", l_dict)
        assert(l_dict is not None)
        out.append((l, l_dict))
    return out

def json_to_weather(data: dict):
    locs = json_to_locations(data)
    print(locs)
    for t in locs:
        id = t[0].location_id
        w:Weather = m.json_data(t[1],id)
        print("got weather object: ", w)
        push(w)

    
    

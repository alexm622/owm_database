#openweathermap python program
from argparse import Namespace
import argparse
import requests
import json
from general_utils import read_secrets 

locs_file: str = "places.csv"

# returns tuple[lon,lat]
def get_coords(location: str, secrets: dict[str, str]) -> tuple[float, float]:
    #break into pieces, format is city_name,country_code,state_code
    state_code = ""
    city_name = location.split(',')[0]
    country_code = location.split(',')[1]
    if location.count(',') > 2:
        state_code = location.split(',')[2]

    request_geocode:str = "http://api.openweathermap.org/geo/1.0/direct?q=$%,$&limit=$&appid=@"
    if state_code != "":
        request_geocode = request_geocode.replace("%", "," + state_code)
    else:
        request_geocode = request_geocode.replace("%", "");

    request_geocode = request_geocode.replace("$", city_name, 1).replace("$", country_code, 1).replace("$",str(1), 1).replace("@", str(secrets.get("owm")))

    response1 = requests.get(request_geocode)

    geocoding: dict = json.loads(response1.text[1: -1])
    geocoding.pop("local_names")

    lat: str | None = str(geocoding.get("lat"))
    lon: str | None = str(geocoding.get("lon"))
    if lat == None or lon == None:
        print("city ", city_name, "failed get request")
        return 0.0,0.0
    else:
        return float(lon), float(lat)



def locations_to_coords(locations: list[str], secrets: dict[str,str]):
    mappings: dict[str, tuple[float,float]] = {}
    for loc in locations:
        coords = get_coords(loc, secrets)
        print(loc)
        statecode = ""
        print("count: ", str(loc.count(",")))
        if loc.count(",") == 2:
            statecode = " " + loc.split(",")[2]
        locname:str = loc.split(',')[0] + " " + loc.split(',')[1] + statecode
        mappings.update({locname: coords})
        
    return mappings

def load_locs():
    global locs_file
    locs: list[str] = []
    f = open(locs_file, "r")
    f.readline() #drop first line
    for s in f:
        if not "," in s:
            continue
        s = s.strip("\n").strip(",") 
        locs.append(s)
    print("locs: ", locs)
    return locs


def write_geodata(data: dict[str, tuple[float,float]]) -> bool:
    f = open("loc_data.csv","w")
    f.write("location,lon,lat\n")
    for s in data.keys():
        print("s: ", s)
        csv_line = s
        tup  = data.get(s)
        lon:float
        lat:float
        if tup == None:
            print("incorrect value in tuple for " + s)
            return False
        else:
            lat = tup[1]
            lon = tup[0]
        csv_line += "," + str(lon) + "," + str(lat)
        print(csv_line)
        f.write(csv_line + "\n")


    return False

def valid_file(file:str) -> bool:
    print("validating file")
    return False

def locnames_to_data(args:Namespace=argparse.ArgumentParser().parse_args()) -> bool:
    if not (len(vars(args)) == 0):
        if not args.geocode:
            print('skipping geocoding')
        if args.LOCS != "":
            if valid_file(args.LOCS):
                global locs_file
                locs_file = args.LOCS
            else:
                print("invalid locs file")
                print("using default (places.csv)")    

    locations: list[str] = load_locs()

    secrets = read_secrets()

    if secrets.get("owm") == "none":
        print("api key not properly defined")
        exit(1)

    coords: dict[str, tuple[float,float]] = locations_to_coords(locations, secrets);

    write_geodata(coords)
    return True









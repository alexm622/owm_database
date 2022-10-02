#location data to weather data
import requests
import time
import os
import json

import general_utils as gu

def build_request(lon: float, lat: float, secrets: dict[str, str] ) -> str:
    
    request_weather:str = "https://api.openweathermap.org/data/2.5/weather?lat=$&lon=$&appid=@"

    request_weather = request_weather.replace("$", str(lat), 1).replace("$", str(lon)).replace("@", str(secrets.get("owm")))

    return request_weather;

def get_weather(lon,lat,secrets)->str:
    req = build_request(lon,lat,secrets)
    print("request: " + req)
    res = requests.get(req).text

    print("response: " + res)

    res = json.loads(res)

    return res

def get_all_weather(locs: dict[str,tuple[float,float]], secrets: dict[str,str]) -> dict:
    out: dict[str,str] = {}
    for s in locs.keys():
        lon,lat = locs[s]
        w:str = get_weather(lon,lat,secrets)
        out.update({s:w})
    return out

def list_to_dict(locs: list[str]) -> dict[str,tuple[float,float]]:
    d: dict[str,tuple[float,float]] = {}
    for s in locs:
        d.update({s.split(",")[0]: (float(s.split(",")[1]), float(s.split(",")[2]))})
    return d 

def load_locdata() -> list[str]:
    out = []
    f = open("loc_data.csv", "r")
    f.readline()

    for s in f:
        s = s.strip("\n").strip(",").strip(" ")
        out.append(s)
    return out

def calc_filename():
    name = ""
    date = time.localtime()
    date = time.strftime("%B-%d-%H",date)
    return name + date + ".json"


def write_json_out(data: dict):
    filename = calc_filename()
    filename = calc_filename()
    if not os.path.exists("data/"):
        os.mkdir("data")
    else:
        if os.path.exists("data/" + filename):
            os.remove("data/" + filename)
    f = open("data/" + filename, "w")
    
    
    f.write(str(data).replace("'","\""))



locs = list_to_dict(load_locdata())

secrets = gu.read_secrets()

aw = get_all_weather(locs, secrets)
print("printing all weather \n\n")
print(aw)

write_json_out(aw)

#location data to weather data
import argparse
import requests
import time
import os
import json
from argparse import ArgumentParser, Namespace

from general_utils import read_secrets

data_file = "loc_data.csv"

def build_request(lon: float, lat: float, secrets: dict[str, str] ) -> str:
    
    request_weather:str = "https://api.openweathermap.org/data/2.5/weather?lat=$&lon=$&appid=@"

    request_weather = request_weather.replace("$", str(lat), 1).replace("$", str(lon)).replace("@", str(secrets.get("owm")))

    return request_weather;

def get_weather(lon,lat,secrets)->str:
    req = build_request(lon,lat,secrets)
    res = requests.get(req).text

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
    
def validate_file(file:str)-> bool:
    return True


def loc_to_weather(args:Namespace|None=None):
    if args != None and len(vars(args)) > 0:
        assert(args is not None)
        if args.output_override != "":
            #override the output
            print("new output")
        if args.loc_data != "":
            if validate_file(args.loc_data):
                #override input file
                global data_file
                data_file = args.loc_data
                print("overriding")
            else:
                print("invalid loc_data file")
                print("using default value (loc_data.csv)")


    locs = list_to_dict(load_locdata())

    secrets = read_secrets()

    aw = get_all_weather(locs, secrets)

    write_json_out(aw)
    #push data
    




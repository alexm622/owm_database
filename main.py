import argparse
from argparse import ArgumentParser, Namespace
import json
import os
import sys

from api_integration.loc_to_weather import loc_to_weather
from api_integration.get_loc_data import locnames_to_data
from database_integration.handler import json_to_weather

import database_integration.push_data as pd

from general_utils import add_args

args: Namespace
parser: ArgumentParser    

def run():
    global args
    if args.push:
        print("pushing weather data to database")
        data = os.listdir("data")
        for file in data:
            path = "data/" + file
            f = open(path)
            aw = ""
            for l in f:
                aw += l
            aw = json.loads(aw)
            json_to_weather(aw)
        print("Done!")
    else:
        print("logging current weather")
        locnames_to_data(args)
        loc_to_weather(args)
        print("done")
    

def init():
    global args, parser
    parser = argparse.ArgumentParser()
    add_args(parser)

    args = parser.parse_args()

    #pd.init()

    
    

def init_locations():
    global args
    locnames_to_data(args)

if __name__ == "__main__":
    init()
    run()

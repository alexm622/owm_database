import argparse
from argparse import ArgumentParser, Namespace
import json

from api_integration.loc_to_weather import loc_to_weather
from api_integration.get_loc_data import locnames_to_data
from database_integration.handler import json_to_weather

from general_utils import add_args

args: Namespace
parser: ArgumentParser    

def run():
    global args
    locnames_to_data(args)
    loc_to_weather(args)

def db_test():
    f = open("api_integration/data/October-02-17.json")
    aw = ""
    for l in f:
        aw += l
    print(aw)
    aw = json.loads(aw)
    print(aw)
    json_to_weather(aw)

def init():
    global args, parser
    print("initializing")
    parser = argparse.ArgumentParser()
    add_args(parser)

    args = parser.parse_args()
    

def init_locations():
    global args
    locnames_to_data(args)

if __name__ == "__main__":
    init()

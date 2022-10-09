import argparse
from argparse import Namespace, ArgumentParser
import json

from api_integration.loc_to_weather import loc_to_weather
from api_integration.get_loc_data import locnames_to_data
from database_integration.handler import json_to_weather

args: Namespace
    

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
    global args
    print("init")
    parser = argparse.ArgumentParser()

    parser = add_args(parser)
    
    args = parser.parse_args()
    print(args)
    

def add_args(parser: ArgumentParser)-> ArgumentParser:
    parser.add_argument('--locs', type=str, help="locations csv file. the format is as follows without quotations:" + 
                        "\"city name\",\"ISO 3166 two letter country code\",\"two letter state code(if applicable)\"",
                        required=False)
    parser.add_argument('--loc-data', type=str, help="location to coordinate override file", required=False)
    parser.add_argument('-o', type=str, help="output file override", required=False, dest='output_override')
    parser.add_argument('-g', action='store_true', default=False, dest='geocode', 
                        help="force retranslate locations to coordinates", required=False)
    parser.add_argument('-p', action='store_true', default=False, dest='push',help="push data to database",
                        required=False)
    parser.add_argument('-po', action='store_true', default=False, dest='only_push',
                        help="push current data to database", required=False)
    parser.add_argument('-ng', action='store_true', default=False, dest='no_get',help="do everything except the final get request", required=False)
    print(parser)
    return parser



def init_locations():
    global args
    locnames_to_data(args)


if __name__ == "__main__":
    locnames_to_data()
    parser = argparse.ArgumentParser()

    parser = add_args(parser)
    
    args = parser.parse_args()


    


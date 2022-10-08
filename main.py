import argparse
import json

import api_integration.loc_to_weather as ltw
import api_integration.get_loc_data as gld
from database_integration.handler import json_to_weather

import database_integration.push_data as pd

import general_utils as gu
    


def run():
    parser = argparse.ArgumentParser()

    gu.add_args(parser)
    
    args = parser.parse_args()

    gld.locnames_to_data(args)
    ltw.loc_to_weather(args)

def db_test():
    f = open("api_integration/data/October-02-17.json")
    aw = ""
    for l in f:
        aw += l
    print(aw)
    aw = json.loads(aw)
    print(aw)
    json_to_weather(aw)

if __name__ == "__main__":
    pd.init()
    db_test()
    


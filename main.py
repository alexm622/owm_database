import argparse

import api_integration.loc_to_weather as ltw
import api_integration.get_loc_data as gld

import database_integration.push_data as pd

import general_utils as gu
    


def run():
    parser = argparse.ArgumentParser()

    gu.add_args(parser)
    
    args = parser.parse_args()

    gld.locnames_to_data(args)
    ltw.loc_to_weather(args)

def db_test():
    pd.test()

if __name__ == "__main__":
    #run()
    db_test()
else:
    print("not main")

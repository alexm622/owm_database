import argparse

import api_integration.loc_to_weather as ltw
import api_integration.get_loc_data as gld
import general_utils as gu
    


def run():
    parser = argparse.ArgumentParser()

    gu.add_args(parser)
    
    args = parser.parse_args()

    gld.locnames_to_data(args)
    ltw.loc_to_weather(args)

if __name__ == "__main__":
    run()
else:
    print("not main")


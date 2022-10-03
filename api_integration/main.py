import argparse

import loc_to_weather as ltw
import get_loc_data as gld
import general_utils as gu

parser = argparse.ArgumentParser()

gu.add_args(parser)

args = parser.parse_args()


gld.locnames_to_data(parser)
ltw.loc_to_weather(parser)

#utils
from argparse import ArgumentParser


def read_secrets():
    secrets: dict[str,str] = {"owm": "none"}

    f = open("secrets.csv", "r")
    f.readline() #drop first line

    #load secrets
    for s in f:
        s = s.strip("\n").strip(",").strip(" ")
        secrets.update({s.split(",")[0]: s.split(",")[1]})
    return secrets

def add_args(parser: ArgumentParser):
    parser.add_argument('--locs', type=str, help="locations csv file. the format is as follows without quotations:" + 
                        "\"city name\",\"ISO 3166 two letter country code\",\"two letter state code(if applicable)\"",
                        required=False)
    parser.add_argument('--loc-data', type=str, help="location to coordinate override file", required=False)

    parser.add_argument('-o', type=str, help="output file override", required=False, dest='output_override')

    parser.add_argument('-g', action='store_true', default=False, dest='geocode', 
                        help="force retranslate locations to coordinates")
    

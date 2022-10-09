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


    
    

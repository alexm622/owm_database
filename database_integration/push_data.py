#push data to sql server

import json

connection_url = ""
connection_uname = ""
connection_passwd = ""
connection_config = "connection_conf.json"
config:dict = {}

def load_config():
    global connection_url,connection_uname,connection_passwd,config
    f = open(connection_config, "r")
    f_conts = "";
    for s in f:
        f_conts += s
    config = json.loads(f_conts)
    print(config)


def push():
    print("push data")

load_config()

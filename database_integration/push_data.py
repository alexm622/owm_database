#push data to sql server

import json

from mysql.connector.connection import MySQLConnection
from mysql.connector.connection_cext import CMySQLConnection
from constant import INSERT_LOCATION

import mysql.connector as connector

connection_url = ""
connection_uname = ""
connection_passwd = ""
connection_config = "connection_conf.json"

#database connection
mydb: MySQLConnection | CMySQLConnection

#load the config file
def load_config():
    global connection_url,connection_uname,connection_passwd
    f = open(connection_config, "r")
    f_conts = "";
    for s in f:
        f_conts += s
    config = json.loads(f_conts)
    print(config)
    connection_url = config.get("url")
    connection_uname = config.get("uname")
    connection_passwd = config.get("passwd") # eventually I want to replace this with secrets.csv
    if connection_passwd == None or connection_uname == None or connection_url == None:
        print("invalid sql config")
        exit(1)
        

#TODO push all the gathered weather data
def push():
    print("push data")

#connect to the database
def connect():
    global mydb, connection_url, connection_uname, connection_passwd
    mydb = connector.connect(host=connection_url, user=connection_uname, password=connection_passwd, database="weather")
    if mydb == None:
        print("bad sql config")
        exit(0)
    assert(mydb is not None)
    print(mydb)

#push the location to the database
def push_location(location_name:str, country_code:str, state_code:str, lon:float, lat:float) -> int:
    global mydb
    vals = (location_name, country_code, state_code, lon, lat)
    cursor= mydb.cursor()
    cursor.execute(INSERT_LOCATION,vals)

    mydb.commit()
    assert(cursor.lastrowid is not None)
    id:int = cursor.lastrowid
    

    
    if id == 0:
        print("id was zero")
        q:list[str] = [(location_name)]
        cursor.execute("SELECT location_id from Locations where location_name = %s LIMIT 1",q)
        fetched = cursor.fetchone()
        assert(fetched is not None)
        fetched = int(fetched[0])
        id = fetched

    print("got id of: " + str(id))

    return id

def get_locations():
    cursor = mydb.cursor()

    cursor.execute("SELECT * FROM Locations")
    result = cursor.fetchall()
    assert(result is not None)

    print(result)
    return result

def test():
    load_config()
    connect()
    push_location("boston","US","MA", 0.0,0.0)
    get_locations()
#push data to sql server

from datetime import datetime
import json

import mysql.connector as connector

from mysql.connector.connection import MySQLConnection
from constant import INSERT_LOC_DATA, INSERT_LOCATION, INSERT_PRECIP, INSERT_TEMP, INSERT_WEATHER, INSERT_WEATHER_TYPES, INSERT_WIND



from datac.location import Location
from datac.mapper import loc_to_datac
from datac.weather import Weather

connection_url = ""
connection_uname = ""
connection_passwd = ""
connection_config = "connection_conf.json"

#database connection
mydb :MySQLConnection

#load the config file
def load_config():
    global connection_url,connection_uname,connection_passwd
    f = open(connection_config, "r")
    f_conts = "";
    for s in f:
        f_conts += s
    config = json.loads(f_conts)
    connection_url = config.get("url")
    connection_uname = config.get("uname")
    connection_passwd = config.get("passwd") # eventually I want to replace this with secrets.csv
    if connection_passwd == None or connection_uname == None or connection_url == None:
        print("invalid sql config")
        exit(1)




#connect to the database
def connect():
    global mydb, connection_url, connection_uname, connection_passwd
    mydb_tmp = connector.connect(host=connection_url, user=connection_uname, password=connection_passwd, database="weather")
    assert(mydb_tmp is MySQLConnection)
    mydb = mydb_tmp
    if mydb == None:
        print("bad sql config")
        exit(0)
    assert(mydb is not None)

def push(weather: Weather):
    cursor = mydb.cursor()
    cursor.execute(INSERT_WEATHER, weather.tup)
    id = cursor.lastrowid
    assert(id is not None)
    if id == 0:
        tup: tuple = (weather.location_id, datetime.fromtimestamp(weather.recorded_date).strftime('%Y-%m-%d %H:%M:%S'))
        cursor.execute("select unique_id from weather_data where location_id=%s and DATE(recorded_date) = DATE(%s)", tup)
        fetched = cursor.fetchone()
        assert(fetched is not None)
        fetched = int(fetched[0])
        id = fetched
        cursor.close()
        return
    cursor.close()
    commit()
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
        q:list[str] = [(location_name)]
        cursor.execute("SELECT location_id from Locations where location_name = %s LIMIT 1",q)
        fetched = cursor.fetchone()
        assert(fetched is not None)
        fetched = int(fetched[0])
        id = fetched
    cursor.close()

    return id

def get_locations():
    global mydb
    cursor = mydb.cursor()

    cursor.execute("SELECT * FROM Locations")
    result = cursor.fetchall()
    assert(result is not None)


    locations: list[Location] = []

    for l in result:
        locations.append(loc_to_datac(l))

    cursor.close()
    return locations


def get_weather_type(weather: dict| None) -> int:
    assert(weather is not None)
    id = -1
    cursor = mydb.cursor()
    cond_code = weather.get("id")
    assert(cond_code is not None)
    cond_code = int(cond_code)
    name = weather.get("main")
    assert(name is not None)
    description = weather.get("description")
    assert(description is not None)
    description = str(description)
    name = str(name)
    icon = None
    #assert(icon is not None)
    input: tuple = (cond_code,name,description,icon)
    cursor.execute(INSERT_WEATHER_TYPES, input)

    id = cursor.lastrowid
    assert(id is not None)

    if id == 0:
        q:list = [(cond_code)]
        cursor.execute("SELECT weather_id from Weather_types where condition_code = %s LIMIT 1",q)
        fetched = cursor.fetchone()
        assert(fetched is not None)
        fetched = int(fetched[0])
        id = fetched
    cursor.close()
    return id

def get_temp_id(temp: dict | None, lid: int, date:int) -> int:
    assert(temp is not None)
    id = -1
    cursor = mydb.cursor()
    temperature = temp.get("temp")
    assert(temperature is not None)
    feels_like = temp.get("feels_like")
    assert(feels_like is not None)
    temp_min = temp.get("temp_min")
    assert(temp_min is not None)
    temp_max = temp.get("temp_max")
    assert(temp_max is not None)
    pressure = temp.get("pressure")
    assert(pressure is not None)
    humidity = temp.get("humidity")
    assert(humidity is not None)
    tup = (lid, temperature, feels_like, temp_min, temp_max, pressure, humidity, datetime.fromtimestamp(date).strftime('%Y-%m-%d %H:%M:%S'))
    cursor.execute(INSERT_TEMP, tup)


    id = cursor.lastrowid
    assert(id is not None)

    if id == 0:
        q: list = [lid,  datetime.fromtimestamp(date).strftime('%Y-%m-%d %H:%M:%S')]
        cursor.execute("SELECT temperature_id FROM temperature_data WHERE location_id = %s AND DATE(recorded_date) = DATE(%s)", q)
        fetched = cursor.fetchone()
        assert(fetched is not None)
        fetched=int(fetched[0])
        id = fetched
    cursor.close()
    return id

def get_wind_id(wind: dict | None, lid: int, date: int) -> int:
    assert(wind is not None)
    speed:float | None = wind.get("speed")
    deg:float | None = wind.get("deg")
    gust:float | None = wind.get("gust")
    assert(speed is not None)
    assert(deg is not None)
    if gust is None:
        gust = 0.0
    assert(gust is not None)
    tup: tuple = (lid, speed, deg, gust, datetime.fromtimestamp(date).strftime('%Y-%m-%d %H:%M:%S'))
    cursor = mydb.cursor()
    cursor.execute(INSERT_WIND, tup)
    tup = (lid,  datetime.fromtimestamp(date).strftime('%Y-%m-%d %H:%M:%S'))
    id = cursor.lastrowid
    assert(id is not None)


    if id == 0:
        cursor.execute("SELECT wind_id FROM wind_data WHERE location_id = %s AND DATE(recorded_date) = DATE(%s)", tup)
        fetched = cursor.fetchone()
        assert(fetched is not None)
        fetched=int(fetched[0])
        id = fetched
    cursor.close()
    return id

def get_precipitation_id(precip: dict | None, lid: int, snow:bool, date:int) -> int:
    id = -1
    assert(precip is not None)
    one_hour = precip.get("1h")
    three_hour = precip.get("3h")
    assert(one_hour is not None)
    assert(three_hour is not None)

    tup = (lid, one_hour, three_hour, snow, datetime.fromtimestamp(date).strftime('%Y-%m-%d %H:%M:%S'))

    cursor = mydb.cursor()

    cursor.execute(INSERT_PRECIP, tup)
    id = cursor.lastrowid
    assert(id is not None)

    if id == 0:
        tup = (lid, datetime.fromtimestamp(date).strftime('%Y-%m-%d %H:%M:%S'))
        cursor.execute("select precipitation_id from precipitation_data where location_id = %s and DATE(recorded_date) = DATE(%s)"
                       " and ", tup)
        fetched = cursor.fetchone()
        assert(fetched is not None)
        fetched=int(fetched[0])
        id = fetched
    cursor.close()
    return id

def get_day_loc(dl: dict | None, lid: int, timezone:int) -> int:
    assert(dl is not None)
    id = -1

    sunrise = dl.get("sunrise")
    sunset = dl.get("sunset")
    assert(sunrise is not None)
    assert(sunset is not None)
    sunrise = datetime.fromtimestamp(sunrise).strftime('%Y-%m-%d %H:%M:%S')
    sunset = datetime.fromtimestamp(sunset).strftime('%Y-%m-%d %H:%M:%S')

    tup:tuple = (lid, sunrise, sunset, timezone)

    cursor = mydb.cursor()
    cursor.execute(INSERT_LOC_DATA, tup)

    id = cursor.lastrowid
    assert(id is not None)

    if id == 0:
        cursor.execute("select day_data_id from day_data where location_id = %s and DATE(sunrise) = DATE(%s)"
                       " and DATE(sunset) = DATE(%s) and timezone = %s LIMIT 1", tup)
        fetched = cursor.fetchone()
        assert(fetched is not None)
        fetched = int(fetched[0])
        id = fetched

    cursor.close()
    return id

def commit():
    mydb.commit()


def init():
    load_config()
    connect()

def close():
    global mydb
    mydb.close()

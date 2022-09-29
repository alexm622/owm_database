#openweathermap python program
from re import split
import requests
import json

def build_request(city_name: str, country_code: str, secrets: dict[str, str], state_code:str="" ) -> str:
    request_geocode:str = "http://api.openweathermap.org/geo/1.0/direct?q=$%,$&limit=$&appid=@"
    if state_code != "":
        request_geocode = request_geocode.replace("%", "," + state_code)
    else:
        request_geocode = request_geocode.replace("%", "");

    request_geocode = request_geocode.replace("$", city_name, 1).replace("$", country_code, 1).replace("$",str(1), 1).replace("@", str(secrets.get("owm")))
    print(request_geocode.replace(str(secrets.get("owm")), "secret"))

    response1 = requests.get(request_geocode)

    geocoding: dict = json.loads(response1.text[1: -1])
    geocoding.pop("local_names")

    print("lon: ", str(geocoding.get("lon")))
    print("lat: ", str(geocoding.get("lat")))
    
    request_weather:str = "https://api.openweathermap.org/data/2.5/weather?lat=$&lon=$&appid=@"
    return ""

f = open("secrets.csv", "r")

secrets: dict[str,str] = {"owm": "none"}

#load secrets
for s in f:
    s = s.strip("\n")
    secrets.update({s.split(",")[0]: s.split(",")[1]})

build_request("boston", "us", secrets, state_code="ma")






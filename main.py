#openweathermap python program
import requests
import json

def build_request(lat: float, lon: float, secrets: dict[str, str] ) -> str:
    
    request_weather:str = "https://api.openweathermap.org/data/2.5/weather?lat=$&lon=$&appid=@"

    request_weather = request_weather.replace("$", str(lat), 1).replace("$", str(lon)).replace("@", str(secrets.get("owm")))

    return request_weather;
# returns tuple[lon,lat]
def get_coords(location: str, secrets: dict[str, str]) -> tuple[float, float]:
    #break into pieces, format is city_name,country_code,state_code
    state_code = ""
    city_name = location.split(',')[0]
    country_code = location.split(',')[1]
    if location.count(',') > 2:
        state_code = location.split(',')[2]

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

    lat: str | None = str(geocoding.get("lat"))
    lon: str | None = str(geocoding.get("lon"))
    if lat == None or lon == None:
        print("city ", city_name, "failed get request")
        return 0.0,0.0
    else:
        return float(lon), float(lat)



def locations_to_coords(locations: list[str], secrets: dict[str,str]):
    mappings: dict[str, tuple[float,float]] = {}
    for loc in locations:
        coords = get_coords(loc, secrets)
        mappings.update({loc.split(',')[0] + " " + loc.split(',')[1]: coords})
    return mappings


    

f = open("secrets.csv", "r")

locations = ["Boston,US,MA", "New York City,US,NY","Dublin,IE"]

loc_to_coords: dict;



secrets: dict[str,str] = {"owm": "none"}

#load secrets
for s in f:
    s = s.strip("\n")
    secrets.update({s.split(",")[0]: s.split(",")[1]})

coords: dict[str, tuple[float,float]] = locations_to_coords(locations, secrets);







#openweathermap python program
import requests
import json
import general_utils as gu 
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

def load_locs():
    locs: list[str] = []
    f = open("places.csv", "r")
    f.readline() #drop first line
    for s in f:
        if not "," in s:
            continue
        s = s.strip("\n").strip(",")
        print(s)
        locs.append(s)
    return locs

def write_geodata(data: dict[str, tuple[float,float]]) -> bool:
    f = open("loc_data.csv","w")
    f.write("location,lon,lat\n")
    for s in data.keys():
        
        csv_line = s
        tup  = data.get(s)
        lon:float
        lat:float
        if tup == None:
            print("incorrect value in tuple for " + s)
            return False
        else:
            lat = tup[1]
            lon = tup[0]
        csv_line += "," + str(lon) + "," + str(lat)
        print(csv_line)
        f.write(csv_line + "\n")


    return False

def locnames_to_data() -> bool:
    locations: list[str] = load_locs()

    secrets = gu.read_secrets()

    if secrets.get("owm") == "none":
        print("api key not properly defined")
        exit(1)

    coords: dict[str, tuple[float,float]] = locations_to_coords(locations, secrets);

    write_geodata(coords)
    return True

if __name__ == "__main__":
    locnames_to_data()











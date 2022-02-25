from pathlib import Path
import requests
import json
import sys
import time
from time import gmtime, strftime

'''TODO
- Compare places
- Weather for specific date
'''


'''Default values'''
headers = {'User-Agent':'jesperdahl@hotmail.no'}
place = 'Oslo'
debug = False

#https://developer.yr.no/doc/StatusCodes/
#https://developer.yr.no/doc/locationforecast/HowTO/
#https://developer.yr.no/doc/GettingStarted/
#https://developer.yr.no/doc/ForecastJSON/

#https://nominatim.openstreetmap.org/search.php?q=oslo&format=jsonv2
#https://api.met.no/weatherapi/locationforecast/2.0/compact?lat=59&lon=10

args = sys.argv

if len(args) == 2:
    place = args[1]
if len(args) == 3:
    place = args[1]
    debug = True if args[2] == '-d' else False


'''Request and processing for lat/lon'''
def request_nomatim(place):
    try:
        base_url = f'https://nominatim.openstreetmap.org/search.php?q={place}&format=jsonv2'
        response = requests.get(base_url, headers={'User-Agent': 'jesperdahl@hotmail.no'})
    except:
        print(f"An error occured, could not access {base_url}")
    return response.json()

def parse_coord(response) -> list() :
    return [float(response[0]['lat']), float(response[0]['lon'])]

def current_time():
    return time.strftime('%a, %d %b %Y %H:%M:%S %Z', time.gmtime())

def write_meta_data(response):
    last_modified = response.headers['Last-Modified']
    expires = response.headers['Expires']

    metadata = {
            'place':place,
            'expires':expires,
            'last_modified':last_modified
        }
    metadata_json = json.dumps(metadata, indent=4)
    with open('metadata.json', 'w') as out_meta:
        out_meta.write(metadata_json)

def write_weather_data(data):
    weather_json_data = json.dumps(data, indent=4)

    with open("weather_data.json", 'w') as outfile:
        outfile.write(weather_json_data)

def direction(deg):
    dirs = ['N', 'NNE', 'NE', 'ENE', 'E', 'ESE', 'SE', 'SSE', 'S', 'SSW', 'SW', 'WSW', 'W', 'WNW', 'NW', 'NNW']
    ix = round(deg / (360. / len(dirs)))
    return dirs[ix % len(dirs)]


def handle_met_request(lat,lon):
    meta_exists = False
    is_modified = False
    last_modified = ""
    expires = ""

    if debug:
        print("Search coords:", lat, lon)
    lat = float(lat)
    lon = float(lon)

    meta_file = Path('metadata.json')
    if meta_file.is_file():
        meta_exists = True

    if not meta_exists:
        if debug:
            print("No previous forecast found, creating new metadata and weatherdata")


        met_response = met_request(lat,lon,is_modified, last_modified)

        if met_response.status_code != 200:
            print("Program exited with code", met_response.status_code)
            exit()
        
        write_meta_data(met_response)
        write_weather_data(met_response.json())

        return met_response.json()

    with open('metadata.json', 'r') as meta_in:
        metadata = json.load(meta_in)
        expires = metadata['expires']
        last_modified = metadata['last_modified']
        meta_place = metadata['place']

        if debug:
            print(f"Metadata found for place {meta_place}: \n Prev. Data expires: {expires}\n Last modified: {last_modified}")
    
    

    if meta_place != place:
        met_response = met_request(lat,lon,is_modified,last_modified)
        write_meta_data(met_response)
        write_weather_data(met_response.json())
        return met_response.json()

    time = current_time()
    if time > expires:
        if debug:
            print(time)
            print("Weather data expired, requesting...")


        is_modified = True
        met_response = met_request(lat,lon,is_modified,last_modified)
        
        if met_response.status_code == 304:
            if debug:
                print("Data not modified, using stored data")
            

            with open('weather_data.json', 'r') as weather_in:
                weather_data = json.load(weather_in)
                return weather_data
        
        write_meta_data(met_response)
        write_weather_data(met_response.json())
        return met_response.json()

    if debug:
        print("Weather data not expired, using stored data")

    with open('weather_data.json', 'r') as weather_in:
        weather_data = json.load(weather_in)
        return weather_data


def show_forecast(response):
    updated_at = response['properties']['meta']['updated_at']
    temp_unit = response['properties']['meta']['units']['air_temperature']

    time = response['properties']['timeseries'][0]['time']
    air_temp = response['properties']['timeseries'][0]['data']['instant']['details']['air_temperature']
    wind_direction = response['properties']['timeseries'][0]['data']['instant']['details']['wind_from_direction']
    wind_speed = response['properties']['timeseries'][0]['data']['instant']['details']['wind_speed']
    
    next_1_hour = {
        #'rain': response['properties']['timeseries'][0]['data']['next_1_hour']['details']['precipitation_amount']
    }

    
    print(f"\n~~~~~~~~ Weather for {place} at {time} ~~~~~~~~")
    print(f"| Updated at {updated_at}\n|")
    print(f"| - {air_temp} degrees {temp_unit}\n| - Wind speed {wind_speed} m/s")
    print(f"| - Wind direction {direction(wind_direction)}")



''' @lat latitude float
    @lon longitude float
    @is_modified boolean if modified since last request
    @modified timestamp 
'''
def met_request(lat, lon, is_modified, modified):
    try:
        base_url = f'https://api.met.no/weatherapi/locationforecast/2.0/compact?lat={lat:.2f}&lon={lon:.2f}'
        if is_modified:
            response = requests.get(base_url, headers={'User-Agent': 'jesperdn@hotmail.no', 'If-Modified-Since':modified})
        else:
            response = requests.get(base_url, headers={'User-Agent': 'jesperdn@hotmail.no'})
    except:
        print(f"An error occured, could not access {base_url}")
    return response


def main():
    nomatim_response = request_nomatim(place)
    coords = parse_coord(nomatim_response)
    met_response = handle_met_request(coords[0], coords[1])
    show_forecast(met_response)

if __name__ == "__main__":
    main()

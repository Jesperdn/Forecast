
import requests
import json
import sys

'''TODO
- Store response,expires,last-modified as json locally
- Before each request check previous saved data
- If not later than expires, just pull saved data
    - Else request new data, overwrite, show results
- Parse wind-direction
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
        response = requests.get(base_url, headers=headers)
    except:
        print(f"An error occured, could not access {base_url}")
    return response.json()

def parse_coord(response) -> list() :
    return [float(response[0]['lat']), float(response[0]['lon'])]
    


def direction(deg):
    dirs = ['N', 'NNE', 'NE', 'ENE', 'E', 'ESE', 'SE', 'SSE', 'S', 'SSW', 'SW', 'WSW', 'W', 'WNW', 'NW', 'NNW']
    ix = round(deg / (360. / len(dirs)))
    return dirs[ix % len(dirs)]


def request_met_API(lat,lon):
    if debug:
        print("search coords:", lat, lon)
    lat = float(lat)
    lon = float(lon)
    try:
        base_url = f'https://api.met.no/weatherapi/locationforecast/2.0/compact?lat={lat:.2f}&lon={lon:.2f}'
        response = requests.get(base_url,headers=headers)
    except:
        print(f"An error occured, could not access {base_url}")

    
    if response.status_code != 200:
        print("Program exited with code", response.status_code)
        exit()
    else:

        if debug:
            print("Status code:", response.status_code)
            

        expires = response.headers['Expires']
        last_modified = response.headers['Last-Modified']


        '''
            Do expires-logic here with saving or loading data
        '''
        return response.json()

def show_forecast(response):

    updated_at = response['properties']['meta']['updated_at']
    temp_unit = response['properties']['meta']['units']['air_temperature']

    time = response['properties']['timeseries'][0]['time']
    air_pressure = response['properties']['timeseries'][0]['data']['instant']['details']['air_pressure_at_sea_level']
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

def test():
    #print(get_coord(request_nomatim('Oslo')))
    #coords = get_coord(request_nomatim('Oslo'))
    #request_met_API(coords[0], coords[1])
    response = request_met_API(59.91, 10.73)
    show_forecast(response)

    
def main():
    nomatim_response = request_nomatim(place)
    coords = parse_coord(nomatim_response)
    met_response = request_met_API(coords[0], coords[1])
    show_forecast(met_response)



if __name__ == "__main__":
    main()

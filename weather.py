from inspect import _void
from urllib import response
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



'''Request and processing for lat/lon'''
def request_nomatim(place):
    try:
        base_url = f'https://nominatim.openstreetmap.org/search.php?q={place}&format=jsonv2'
        response = requests.get(base_url, headers=headers)
    except:
        print(f"An error occured, could not access {base_url}")
    return response.json()

def get_coord(response) -> list() :
    return [float(response[0]['lat']), float(response[0]['lon'])]
    




def request_met_API(lat,lon):
    lat = float(lat)
    lon = float(lon)
    try:
        base_url = f'https://api.met.no/weatherapi/locationforecast/2.0/compact?lat={lat:.2f}&lon={lon:.2f}'
        response = requests.get(base_url,headers=headers)
    except:
        print(f"An error occured, could not access {base_url}")

    

    #json.dumps([response])
    if response.status_code != 200:
        print("Program exited with code", response.status_code)
        exit()
    else:
        expires = response.headers['Expires']
        last_modified = response.headers['Last-Modified']
        #print(response.status_code)
        #print(response.headers)

        return response.json()

def show_forecast(response):

    updated_at = response['properties']['meta']['updated_at']
    temp_unit = response['properties']['meta']['units']['air_temperature']

    time = response['properties']['timeseries']['time']
    air_pressure = response['properties']['timeseries']['data']['instant']['air_pressure_at_sea_level']
    air_temp = response['properties']['timeseries']['data']['instant']['air_temperature']
    wind_direction = response['properties']['timeseries']['data']['instant']['wind_from_direction']
    wind_speed = response['properties']['timeseries']['data']['instant']['wind_speed']

    next_hour = {
        'wind': response['properties']['timeseries']['data']['next_1_hours']['wind_speed'],
        'air_temp': response['properties']['timeseries']['data']['next_1_hours']['air_temperature'],
        'mm': response['properties']['timeseries']['data']['next_1_hours']['air_temperature']
    }
    
    print(f"\n~~~~~~~~ Weather for {place} at {time} ~~~~~~~~")
    print(f"| Updated at {updated_at}")
    print(f"\n| - {air_temp} degrees {temp_unit}\n| - ")

def test():
    #print(get_coord(request_nomatim('Oslo')))
    #coords = get_coord(request_nomatim('Oslo'))
    #request_met_API(coords[0], coords[1])
    response = request_met_API(59.91, 10.73)
    show_forecast(response)

    


if __name__ == "__main__":
    
    test()

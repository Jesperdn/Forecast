import sys
import argparse

import requests
import pandas as pd
import rich

global debug



# //// Get location coordinates ////

def get_location_coords(location) -> pd.DataFrame :
  """
  Gets the coordinates of a gived location based on the location name.

  Uses openstreetmap:
    https://nominatim.openstreetmap.org/search.php?q=oslo&format=jsonv2

  Args: 
    location: the location to get coords from

  Returns:
    a Pandas DataFrame containing necessary information on the given loc

  """
  nomatim_url: str = f'https://nominatim.openstreetmap.org/search.php?q={location}&format=jsonv2'
  
  try:
      response: str = requests.get(nomatim_url, headers={
        'User-Agent': 'test@testesen.com'
      }).text
  except Exception:
    print(f'<Error> could not access {nomatim_url}')
    exit(1)
  
  return pd.read_json(response)[['place_id', 'display_name', 'boundingbox']]

def test_get_location_coords(location="Oslo") -> None :
  """
  Test get_location_coords function. Print result.

  Args:
    location: test location

  Returns:
    None
  """

  print(get_location_coords(location=location))




def main():
  
  parser = argparse.ArgumentParser()

  # // Required args //
  parser.add_argument("location", help="The forecast location.")
  
  # // Optional args //
  parser.add_argument("-d", "--debug", help="Debug mode.", action='store_true')

  args = vars(parser.parse_args())

  debug: bool = args['debug'] 
  location: str = args['location']
  



  # // TEST // 
  test_get_location_coords()






# //// ENTRY ////
 
if __name__=="__main__":
  main()
import urllib.request
import json
from pprint import pprint

# Useful URLs (you need to add the appropriate parameters for your requests)
MAPQUEST_BASE_URL = "http://open.mapquestapi.com/geocoding/v1/address"
MBTA_BASE_URL = "https://api-v3.mbta.com/stops"

# Your API KEYS (you need to use your own keys - very long random characters)
MAPQUEST_API_KEY = "lTwUivJmv5fVNxOs7uBvRLgn8EA5VCIm"
MBTA_API_KEY = "c7f0bef048684f6b8e311472dc266776"
url = "http://open.mapquestapi.com/geocoding/v1/address?key={}&location={}"

# A little bit of scaffolding if you want to use it

def get_json(url,place_name):
   """
   Given a properly formatted URL for a JSON web API request, return
   a Python JSON object containing the response to that request.
   """
   url = url.format(MAPQUEST_API_KEY,place_name)
   f = urllib.request.urlopen(url)
   response_text = f.read().decode('utf-8')
   response_data = json.loads(response_text)
   return response_data


def get_lat_long(response_data):
   """
   Given a place name or address, return a (latitude, longitude) tuple
   with the coordinates of the given place.
   See https://developer.mapquest.com/documentation/geocoding-api/address/get/
   for Mapquest Geocoding  API URL formatting requirements.
   """
   latitude = response_data['results'][0]['locations'][0]['displayLatLng']['lat']
   longitude = response_data['results'][0]['locations'][0]['displayLatLng']['lng']
   return latitude,longitude

def get_nearest_station(latitude, longitude):
   """
   Given latitude and longitude strings, return a (station_name, wheelchair_accessible)
   tuple for the nearest MBTA station to the given coordinates.
   See https://api-v3.mbta.com/docs/swagger/index.html#/Stop/ApiWeb_StopController_index for URL
   formatting requirements for the 'GET /stops' API.
   """
   url_mbta = "{}?api_key={}&filter[latitude]={}&filter[longitude]={}&filter[radius]=0.04'".format(MBTA_BASE_URL,MBTA_API_KEY,latitude,longitude)
   print(url_mbta)
   f = urllib.request.urlopen(url_mbta)
   response_text = f.read().decode('utf-8')
   response_data = json.loads(response_text)
   # return response_data
   if len(response_data['data'])==0:
       near_stop = 'No Information'
       wheelchair = 'No Information'
       return near_stop,wheelchair
   near_stop = response_data['data'][0]['attributes']['name']
   wheelchair = response_data['data'][0]['attributes']['wheelchair_boarding']
   if wheelchair == 0:
       access_info = 'No Information about Wheelchair'
   elif wheelchair == 1:
       access_info = 'Wheelchair is accessible (if trip is wheelchair accessible)'
   elif wheelchair == 2:
       access_info = 'Wheelchair is inaccessible'
   return near_stop,access_info

def find_stop_near(place_name):
   """
   Given a place name or address, return the nearest MBTA stop and whether it is wheelchair accessible.
   """
   while ' ' in place_name:
       idx = place_name.index(' ')
       place_name = place_name[0:idx]+'+'+place_name[idx+1:]
   data = get_json(url,place_name)
   latitude,longitude = get_lat_long(data)
   return get_nearest_station(latitude,longitude)



def main():
   """
   You can all the functions here
   """
   # data = get_json(url,"Framingham")
   # latitude,longtitude = get_lat_long(data)
   # print(latitude,longtitude)
   # pprint(get_nearest_station(latitude,longtitude))

if __name__ == '__main__':
   main()

import requests
import json
from datetime import datetime

def get_localization() -> tuple:
    """function returns tuple with latitude and longtitude based on IP
        return: (latitude, longitude) or status code if its different than 200
        WARNING: function works only if you host app
    """
    global CITY
    url: str = 'https://ipinfo.io' # site which returns your geolocation based on IP

    response = requests.get(url)
    if response.status_code != 200: # if connection failed return status code
        return response.status_code 
    
    response_dict: dict = json.loads(response.text)
    # tuple with localization values as float
    CITY = response_dict['city']
    localization = tuple(map(float, response_dict['loc'].split(',')))
    return localization

CITY: str = '' # current user city
UNITS: dict = {} # dict which will store units for data

def get_data() -> dict:
    """function returns data from API"""
    global UNITS
    url: str = 'https://api.open-meteo.com/v1/forecast' # free weather API
    
    latitude: float = 0.0
    longitude: float = 0.0
    localization = get_localization()
    if isinstance(localization, tuple):
        latitude, longitude = localization

    params: dict = {
        'latitude': latitude,
        'longitude': longitude,
        'forecast_days': 1,
        'hourly': ["temperature_2m", "relative_humidity_2m", "precipitation_probability", "surface_pressure", "cloud_cover", "wind_speed_10m", "wind_direction_10m"]
    }
    
    response = requests.get(url, params)
    if response.status_code != 200:
        return response.status_code
    
    response_dict: dict = json.loads(response.text)
    UNITS = response_dict['hourly_units'] # store units in constant
    
    return response_dict['hourly']

def prepare_data_to_current_hour() -> dict:
    now: str = datetime.now()
    formatted: str = now.strftime('%Y-%m-%dT%H:00')
    data = get_data()
    index: int = data['time'].index(formatted)
    for key in data:
        data[key] = data[key][22:]
    return data

import requests
import json
from datetime import datetime
import ipaddress

def is_private_ip(ip: str):
    try:
        ip_obj = ipaddress.ip_address(ip)
        private_networks: list = [
            ipaddress.IPv4Network('10.0.0.0/8'),
            ipaddress.IPv4Network('172.16.0.0/12'),
            ipaddress.IPv4Network('192.168.0.0/16'),
        ]
        for private_network in private_networks:
            if ip_obj in private_network:
                return True
        return False
    except:
        return False

def get_localization(ip: str='') -> tuple:
    """function returns tuple with latitude and longtitude based on IP
        return: (latitude, longitude) or status code if its different than 200
        WARNING: function works only if you host app
    """
    url: str = 'https://ipinfo.io/' # site which returns your geolocation based on IP
    url = url if is_private_ip(ip) else url + ip
    print(ip)

    response = requests.get(url)
    if response.status_code != 200: # if connection failed return status code
        return response.status_code 
    
    response_dict: dict = json.loads(response.text)
    # tuple with localization values as float
    city = response_dict['city']
    localization = tuple(map(float, response_dict['loc'].split(',')))
    return (localization, city)

UNITS: dict = {} # dict which will store units for data #NOTE: can cause problems with more users but is not necessary to fix

def get_data(ip: str = '') -> dict:
    """function returns data from API"""
    global UNITS
    url: str = 'https://api.open-meteo.com/v1/forecast' # free weather API
    
    latitude: float = 0.0
    longitude: float = 0.0
    localization = get_localization(ip)[0]
    if isinstance(localization, tuple):
        latitude, longitude = localization

    params: dict = {
        'latitude': latitude,
        'longitude': longitude,
        'forecast_days': 2,
        'hourly': ["temperature_2m", "relative_humidity_2m", "precipitation_probability", "surface_pressure", "cloud_cover", "wind_speed_10m", "wind_direction_10m"]
    }
    
    response = requests.get(url, params)
    if response.status_code != 200:
        return response.status_code
    
    response_dict: dict = json.loads(response.text)
    UNITS = response_dict['hourly_units'] # store units in constant
    
    return response_dict['hourly']

def wind_direction(direction: int) -> str:
    if direction < 23 or direction > 338:
        return 'N'
    if 23 < direction < 68:
        return 'NE'
    if 68 < direction < 113:
        return 'E'
    if 113 < direction < 158:
        return 'SE'
    if 158 < direction < 203:
        return 'S'
    if 203 < direction < 248:
        return 'SW'
    if 248 < direction < 338:
        return 'W'

def prepare_data_to_current_hour(ip: str = '') -> dict:
    now: str = datetime.now()
    now_formatted: str = now.strftime('%Y-%m-%dT%H:00')
    data = get_data(ip)
    index: int = data['time'].index(now_formatted)
    for key in data:
        data[key] = data[key][index:(index + 26)]
    for index in range(len(data['time'])):
        data['time'][index] = ' - '.join(data['time'][index][5:].replace('-', '/').split('T'))
    for index in range(len(data['wind_direction_10m'])):
        data['wind_direction_10m'][index] = wind_direction(data['wind_direction_10m'][index])
    return data

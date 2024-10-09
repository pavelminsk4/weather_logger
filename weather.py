from dotenv import load_dotenv
from retry_requests import retry
import os
import openmeteo_requests
import requests_cache

load_dotenv()

api_url = os.getenv('API_URL')
lat = os.getenv('LATITUDE')
lon = os.getenv('LONGITUDE')


def fetch_weather():
    # Setup the Open-Meteo API client with cache and retry on error
    cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
    retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
    openmeteo = openmeteo_requests.Client(session=retry_session)

    # Make sure all required weather variables are listed here
    # The order of variables in hourly or daily is important to assign them correctly below
    url = api_url
    params = {
        "latitude": lat,
        "longitude": lon,
        "current": ["temperature_2m", "precipitation", "rain", "showers", "snowfall", "surface_pressure", "wind_speed_10m", "wind_direction_10m"]
    }
    responses = openmeteo.weather_api(url, params=params)

    # Process first location. Add a for-loop for multiple locations or weather models
    response = responses[0]

    # Current values. The order of variables needs to be the same as requested.
    current = response.Current()
    current_temperature_2m = current.Variables(0).Value()
    current_precipitation = current.Variables(1).Value()
    current_rain = current.Variables(2).Value()
    current_showers = current.Variables(3).Value()
    current_snowfall = current.Variables(4).Value()
    current_surface_pressure = current.Variables(5).Value()
    current_wind_speed_10m = current.Variables(6).Value()
    current_wind_direction_10m = current.Variables(7).Value()

    data = {
        "current_time": current.Time(),
        "current_temperature_2m": current_temperature_2m,
        "current_precipitation": current_precipitation,
        "current_rain": current_rain,
        "current_showers": current_showers,
        "current_snowfall": current_snowfall,
        "current_surface_pressure": current_surface_pressure,
        "current_wind_speed_10m": current_wind_speed_10m,
        "current_wind_direction_10m": current_wind_direction_10m
    }

    return data

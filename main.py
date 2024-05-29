import streamlit as st
import requests, json
import datetime
import pandas as pd
import pytz
import timezonefinder
from IPython import get_ipython
import argparse
import geocoder



#!pip install streamlit
#!pip install requests
#!pip install json
#!pip install datetime
#!pip install pandas
#!pip install pytz
#!pip install timezonefinder
#!pip install sys
#!pip install IPython
#!pip install argparse
#!pip install geocoder
#!pip install geopy

def check_streamlit():
    try:
        from streamlit.runtime.scriptrunner import get_script_run_ctx
        if not get_script_run_ctx():
            use_streamlit = False
        else:
            use_streamlit = True
    except ModuleNotFoundError:
        use_streamlit = False
    return use_streamlit

def fet_friendly_local_time():
    local_date_time = None
    try:
        g = geocoder.ip('me')
        if g.current_result is not None:
            coordinates = g.latlng
            if coordinates is not None:
                latitude, longitude = coordinates
                local_date_time = get_friendly_datetime(g.current_result.address, longitude, latitude)
        return local_date_time
    except:
        return local_date_time


def get_friendly_datetime(city_name, lon, lat):
    try:
        timezone_str = get_tz_by_location(lon, lat)
        user_timezone = pytz.timezone(timezone_str)

        utc_now = datetime.datetime.utcnow()

        local_time = utc_now.astimezone(user_timezone)

        formatted_time = local_time.strftime("%A, %B %d, %Y %I:%M %p")

        return (f"Current time in {city_name}: {formatted_time}")
    except pytz.UnknownTimeZoneError:
        return (f"Error: '{timezone_str}' is not a valid timezone.")


def get_city_wheather_info(city_name):
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    api_key = "4473ba83f98e561df59a98f254855e99"
    complete_url = base_url + "appid=" + api_key + "&q=" + city_name + "&units=metric"
    if api_key:
        response = requests.get(complete_url)
        x = response.json()
        if "cod" in x:
            return x
        else:
            return None


def get_tz_by_location(lon, lat):
    tf = timezonefinder.TimezoneFinder()
    timezone_str = tf.certain_timezone_at(lat=lat, lng=lon)
    if timezone_str is None:
        timezone_str = tf.closest_timezone_at(lat=lat, lng=lon)
    return timezone_str

def my_print(st1,st2):
    if 'google.colab' in str(get_ipython()):
        print(f"{st1} {st2}")
    elif check_streamlit():
        st.markdown(f"{st1} {st2}")
    else:
        print(f"{st1} {st2}")

use_cli=True
city_name=None
if 'google.colab' in str(get_ipython()) or check_streamlit():
  use_cli=False

if use_cli:
  parser = argparse.ArgumentParser(description='OpenWeatherMap CLI')
  parser.add_argument('--location', type=str, help='Location to get the weather for')
  args = parser.parse_args()

  if args.location:
    city_name = args.location

else:
    if 'google.colab' in str(get_ipython()):
        print("OpenWeatherMap - Moshe Harary")
    elif check_streamlit():
        st.title("OpenWeatherMap - Moshe Harary")
        df = pd.read_csv('https://raw.githubusercontent.com/mosheharary/csvfiles/main/500_cities.csv')
    else:
        print("OpenWeatherMap - Moshe Harary")


if not city_name:
    if 'google.colab' in str(get_ipython()):
        city_name = input("Enter city name: ")
    elif check_streamlit():
        city_name = st.selectbox("Choose City:", df['City'].tolist())
    else:
        city_name = input("Enter city name: ")

wheather = get_city_wheather_info(city_name)

if wheather:
    if wheather["cod"] != "404":
        local_date_time = fet_friendly_local_time()
        date_time = get_friendly_datetime(city_name, wheather['coord']['lon'], wheather['coord']['lat'])
        y = wheather["main"]
        current_temperature = y["temp"]
        fahrenheit_temperature = (current_temperature * 1.8) + 32
        current_pressure = y["pressure"]
        current_humidiy = y["humidity"]
        z = wheather["weather"]
        weather_description = z[0]["description"]
        my_print('Local Time : ', str(local_date_time))
        my_print(city_name + ' Time : ', str(date_time))
        my_print('--------------------------------', "")
        my_print('City : ', str(wheather["name"]))
        my_print('Country : ', str(wheather["sys"]["country"]))
        my_print('Weather Description : ', str(weather_description))
        my_print('Temperature (C/F) : ', str(current_temperature)+"/"+str(fahrenheit_temperature))
        my_print('atmospheric pressure (in hPa unit) : ', str(current_pressure))
        my_print('humidity (in percentage) : ', str(current_humidiy))
    else:
        my_print(city_name," City Not Found ")
# OpenWeatherMap - Weather API
## Description
This is a simple weather API that uses OpenWeatherMap API to get the weather data of a city. The API is built using FastAPI and is deployed on Heroku. The API has a single endpoint that takes the city name as a query parameter and returns the weather data of that city. The weather data includes the temperature, humidity, and weather description of the city.
## Usage
To use the API, send a GET request to the following URL:
```
http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}
```
The code can be used using the folowing methods:
* cli with parameters:
  - location: city name
```
    python main.py --location "city_name"
```
* running as colab [notebook](https://colab.research.google.com/github/mosheharary/OpenWeatherMap/blob/main/DS17_OpenWeatherMap.ipynb):
* run inside streamlit [app](https://openweathermap-dcaxrfco2fuy5xepj5pwxd.streamlit.app/)



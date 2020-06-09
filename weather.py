import requests, json
from secrets import weather_api_key



def find_weather(city):

    # API Key for Khaleesi
    api_key = weather_api_key

    # base url variable to store url
    base_url = "http://api.openweathermap.org/data/2.5/weather?"

    # The city name
    city_name = city

    # Complete url address
    url = base_url + "appid=" + api_key + "&q=" + city_name

    # request the url
    r = requests.get(url)

    # json method of the r object
    x = r.json()

    # Checks the value of cod key
    # 404 city not found
    if x["cod"] != "404":

        # store the value of "main"
        # in the variable y
        y = x["main"]

        # temp is Kelvin - must convert
        current_temp = y['temp']
        # converts k to F
        convert_temp = 1.8 * (current_temp - 273) + 32
        rounded_temp = round(convert_temp)
        return rounded_temp
    else:
        # Cant find city
        return None
        
        



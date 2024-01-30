import requests

APIkey = 'c095965a6e3bd45ae3952f546d9d817d'
def get_weather_by_location(latitude, longitude):
    url = f'https://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&appid={APIkey}'
    url2 = f'http://api.openweathermap.org/geo/1.0/reverse?lat={latitude}&lon={longitude}&limit=2&appid={APIkey}'
    response = requests.get(url).json()
    response2 = requests.get(url).json()
    # response2 = requests.get(url2).json()
    city_name = response2[0]['name']
    weather = response['weather'][0]['description']
    temperature = response['main']['temp']
    feels_like = response['main']['feels_like']
    wind_speed = response['wind']['speed']
    context = {}
    context['weather'] = weather
    context['temperature'] = [float(temperature)-273.15, float(feels_like)-273.15]
    context['wind'] = wind_speed
    context['city'] = city_name
    return context


def get_users():
    url = 'http://127.0.0.1:8000/telegram/users/'
    response = requests.get(url).json()
    return response

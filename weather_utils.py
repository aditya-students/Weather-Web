import requests
import config
from datetime import datetime

def get_weather(city):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={config.API_KEY}&units=metric"
    response = requests.get(url)
    return response.json()

def suggest_clothing(temp, weather):
    if temp < 10:
        return "Wear a warm coat, gloves, and a hat."
    elif temp < 20:
        return "A jacket or sweater would be good."
    elif "rain" in weather.lower():
        return "Carry an umbrella and wear a raincoat."
    else:
        return "Light clothing is fine."

def format_time(timestamp):
    return datetime.utcfromtimestamp(timestamp).strftime("%I:%M %p")

def get_sun_times(city):
    data = get_weather(city)
    sunrise = format_time(data["sys"]["sunrise"])
    sunset = format_time(data["sys"]["sunset"])
    return sunrise, sunset

import speech_recognition as sr
import pyttsx3
from weather_utils import get_weather

engine = pyttsx3.init()

def speak(text):
    if not engine.isBusy():
        engine.say(text)
        engine.runAndWait()


def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening for weather request...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    try:
        return recognizer.recognize_google(audio)
    except sr.UnknownValueError:
        return "Sorry, I didn't catch that."

def voice_weather():
    speak("Which city's weather would you like to know?")
    city = listen()
    weather_data = get_weather(city)
    if weather_data["cod"] == 200: 
        print(f"The temperature in {city} is {weather_data['main']['temp']} degrees Celsius with {weather_data['weather'][0]['description']}.")

        temp = weather_data["main"]["temp"]
        description = weather_data["weather"][0]["description"]
        print(f"The temperature in {city} is {temp} degrees Celsius with {description}.")
        speak(f"The temperature in {city} is {temp} degrees Celsius with {description}.")

    else:
        speak("I couldn't find that city. Please try again.")

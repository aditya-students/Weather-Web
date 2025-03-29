from flask import Flask, render_template, request, jsonify
from weather_utils import get_weather, suggest_clothing, get_sun_times
import pyttsx3
import threading

app = Flask(__name__)
engine = pyttsx3.init()

def speak(text):
    def run():
        engine.say(text)
        engine.runAndWait()
    thread = threading.Thread(target=run)
    thread.start()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get_weather", methods=["POST"])
def weather():
    city = request.form["city"]
    weather_data = get_weather(city)
    if weather_data["cod"] == 200:
        temp = weather_data["main"]["temp"]
        description = weather_data["weather"][0]["description"]
        wind_speed = weather_data["wind"]["speed"]
        sunrise, sunset = get_sun_times(city)
        clothing_suggestion = suggest_clothing(temp, description)

        # Determine background image based on weather
        weather_condition = description.lower()
        if "cloud" in weather_condition:
            bg_image = "cloudy.jpg"
        elif "rain" in weather_condition:
            bg_image = "rainy.jpg"
        elif "snow" in weather_condition:
            bg_image = "snow.jpg"
        elif "clear" in weather_condition:
            bg_image = "sunny.jpg"
        else:
            bg_image = "weather_bg.jpg"

        weather_text = (f"The temperature in {city} is {temp} degrees Celsius. "
                        f"The weather is {description}. The wind speed is {wind_speed} meters per second. "
                        f"Sunrise is at {sunrise}, and sunset is at {sunset}. "
                        f"Recommended clothing: {clothing_suggestion}.")

        return jsonify({
            "temperature": temp,
            "weather": description,
            "wind_speed": wind_speed,
            "sunrise": sunrise,
            "sunset": sunset,
            "clothing_suggestion": clothing_suggestion,
            "weather_text": weather_text,
            "background_image": bg_image
        })
    else:
        return jsonify({"error": "City not found"}), 404


@app.route("/speak_weather", methods=["POST"])
def speak_weather():
    data = request.get_json()
    text = data.get("text", "")
    speak(text)  # Now runs in a separate thread
    return jsonify({"status": "Speaking"})

if __name__ == "__main__":
    app.run(debug=True)

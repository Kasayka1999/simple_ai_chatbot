import json
import requests


def get_geocoding_of_city(city):
    # get latitude and longitude from open-meteo geocoding API
    url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}"
    response = requests.get(url)

    if response.status_code != 200:
        print("[ERROR] Failed to fetch geocoding data.")
        return None, None

    city_data = response.json()
    results = city_data["results"]
    for result in results:
        latitude = result["latitude"]
        longitude = result["longitude"]
    return latitude, longitude  # last match returned


def get_user_question():
    # ask question to UX-AI
    question = input("Please ask UX-AI what to wear today: ")
    return question


def get_weather(latitude, longitude):
    # get current weather using open-meteo forecast API
    url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current=temperature_2m"
    response = requests.get(url)

    if response.status_code != 200:
        print("[ERROR] Failed to fetch weather data.")
        return None

    weather_data = response.json()
    return weather_data


def get_ai_response(weather_data, user_question):
    # send weather and question to OpenAI Chat Completion API
    URL = "https://api.openai.com/v1/chat/completions"
    OPENAI_KEY = "YOUR_KEY"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {OPENAI_KEY}"
    }
    payload = {
        "model": "gpt-4o-mini",
        "messages": [{
            "role": "user",
            "content": (
                f"Here is the weather for today: {weather_data} "
                f"Here is the question from a user: {user_question} "
                f"Please answer the question."
            )
        }]
    }

    response = requests.post(URL, data=json.dumps(payload), headers=headers)

    if response.status_code != 200:
        print("[ERROR] Failed to get AI response.")
        return

    returned_context = response.json()["choices"][0]
    print(returned_context["message"]["content"])


def main():
    # get user input for city
    get_user_city = input("Please type your city: ")

    # get the geodata (latitude, longitude)
    city_latitude, city_longitude = get_geocoding_of_city(get_user_city)

    # if location failed
    if city_latitude is None or city_longitude is None:
        return

    # get weather info using coordinates
    weather_data = get_weather(city_latitude, city_longitude)

    if weather_data is None:
        return

    # get question from user
    user_question = get_user_question()

    # send question and weather to AI
    get_ai_response(weather_data, user_question)


if __name__ == "__main__":
    main()
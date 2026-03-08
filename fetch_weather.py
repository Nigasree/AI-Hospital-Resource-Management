import requests

API_KEY = "fd99fd76e41977d92adafd06f7186b59"

def get_weather_data():

    url = f"https://api.openweathermap.org/data/2.5/weather?q=Chennai&appid={API_KEY}&units=metric"

    response = requests.get(url)

    data = response.json()

    # Check if API returned valid data
    if "main" not in data:
        print("API Error:", data)
        return None

    weather_info = {
        "temperature": data["main"]["temp"],
        "rainfall": data.get("rain", {}).get("1h", 0)
    }

    return weather_info


# Test the API
if __name__ == "__main__":

    weather = get_weather_data()

    print("Weather Data:", weather)
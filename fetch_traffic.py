import requests

API_KEY = "LMob4VVqCiSNt9EVg15EhzHSow1SdWVv"

def get_traffic_data():

    url = f"https://api.tomtom.com/traffic/services/4/flowSegmentData/absolute/10/json?point=13.0827,80.2707&key={API_KEY}"

    response = requests.get(url)

    data = response.json()

    traffic_level = data["flowSegmentData"]["currentSpeed"]

    # Convert traffic speed into approximate accident signal
    accident_reports = 0

    if traffic_level < 20:
        accident_reports = 6
    elif traffic_level < 40:
        accident_reports = 3
    else:
        accident_reports = 1

    return accident_reports


if __name__ == "__main__":

    accidents = get_traffic_data()

    print("Estimated Accident Reports:", accidents)
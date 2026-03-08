from fetch_weather import get_weather_data
from fetch_traffic import get_traffic_data
import joblib
import pandas as pd

model = joblib.load("hospital_prediction_model.pkl")

weather = get_weather_data()
accidents = get_traffic_data()

input_data = {
    "temperature": weather["temperature"],
    "rainfall": weather["rainfall"],
    "accident_reports": accidents,
    "disease_cases": 12,
    "emergency_cases": 20,
    "waiting_time_minutes": 30,
    "day_of_week": 2,
    "month": 4
}

df = pd.DataFrame([input_data])

prediction = model.predict(df)

print("Predicted Patient Inflow:", int(prediction[0]))
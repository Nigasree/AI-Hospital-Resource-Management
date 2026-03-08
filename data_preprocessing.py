import pandas as pd

def preprocess_data(data):

    data['date'] = pd.to_datetime(data['date'])

    data['day_of_week'] = data['date'].dt.dayofweek
    data['month'] = data['date'].dt.month

    features = [
        'temperature',
        'rainfall',
        'accident_reports',
        'disease_cases',
        'emergency_cases',
        'waiting_time_minutes',
        'day_of_week',
        'month'
    ]

    X = data[features]
    y = data['patient_count']

    return X, y
import random

def get_nearby_hospitals():

    hospitals = [
        {"name": "City Hospital", "patients": random.randint(40,120), "beds_available": 30},
        {"name": "Metro Care", "patients": random.randint(30,100), "beds_available": 20},
        {"name": "Green Valley Hospital", "patients": random.randint(50,150), "beds_available": 25}
    ]

    return hospitals
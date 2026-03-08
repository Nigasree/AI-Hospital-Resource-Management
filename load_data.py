import mysql.connector
import pandas as pd

def load_data():

    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="hospital_ai"
    )

    query = "SELECT * FROM hospital_dataset"

    data = pd.read_sql(query, connection)

    return data
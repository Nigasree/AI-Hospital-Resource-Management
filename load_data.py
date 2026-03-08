def load_data():

    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="hospital_ai"
    )

    query = """
    SELECT *
    FROM hospital_dataset
    ORDER BY date DESC
    LIMIT 50
    """

    df = pd.read_sql(query, connection)

    connection.close()

    return df

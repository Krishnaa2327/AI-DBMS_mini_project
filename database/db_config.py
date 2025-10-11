import mysql.connector
from mysql.connector import Error

def get_connection():
    try:
        connection = mysql.connector.connect(
            host="localhost",        # change if using remote DB
            user="root",             # your MySQL username
            password="Krishna@112406", # your MySQL password
            database="smart_hospital" # database name you’ll create
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print("Error while connecting to MySQL:", e)
        return None

import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="myuser",
        password="mypassword",
        database="simpledb"
    )

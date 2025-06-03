import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="FastAPI",            # तुझं MariaDB user नांव
        password="3011",           # user password
        database="simpledb"
    )

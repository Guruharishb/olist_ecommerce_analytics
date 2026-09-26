import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="MYPASS",
        password="root",
        database="olist_analytics"
    )
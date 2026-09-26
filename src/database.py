import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="Your_Pass",
        password="root",
        database="olist_analytics"
    )
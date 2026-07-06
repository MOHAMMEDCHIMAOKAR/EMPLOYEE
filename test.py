import mysql.connector

try:
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Root",
        database="emp"
    )
    print("Database connection successful")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM employees")
    print("Query successful")
    print(cursor.fetchall())
except mysql.connector.Error as e:
    print(f"Error: {e}")
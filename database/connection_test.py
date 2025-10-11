import mysql.connector

try:
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Krishna@112406",
        database="smart_hospital"
    )
    print("✅ MySQL connection successful!")
except Exception as e:
    print("❌ Error:", e)
finally:
    if conn.is_connected():
        conn.close()
        print("MySQL connection closed.")
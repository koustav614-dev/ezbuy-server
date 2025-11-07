import mysql.connector

def get_connection():
    try:
        connection = mysql.connector.connect(
            host="localhost",       # or IP if using remote server
            user="root",            # your MySQL username
            password="Abhijit@99",  # your MySQL password
            database="ezbuy"        # the database you created in Workbench
        )

        if connection.is_connected():
            print("✅ Connected to MySQL database")
        return connection

    except mysql.connector.Error as e:
        print("❌ Error while connecting to MySQL", e)
        return None

# Test connection
if __name__ == "__main__":
    conn = get_connection()
    if conn:
        conn.close()

from db_connect import get_connection

def create_table():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS registration (
            id INT AUTO_INCREMENT PRIMARY KEY,
            Username VARCHAR(100) NOT NULL UNIQUE,
            Email VARCHAR(100) NOT NULL UNIQUE,
            Pass VARCHAR(255) NOT NULL
        )
    """)

    conn.commit()
    print("✅ Table 'registartion' created successfully")

    cursor.close()
    conn.close()

if __name__ == "__main__":
    create_table()

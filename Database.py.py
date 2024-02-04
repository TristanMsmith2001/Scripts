import sqlite3

def create_database():
    # Connect to SQLite database (or create it if it doesn't exist)
    conn = sqlite3.connect('routers.db')
    cursor = conn.cursor()

    # Create 'routers' table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS routers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        ip_address TEXT UNIQUE NOT NULL,
        username TEXT NOT NULL,
        password TEXT NOT NULL
    )
    ''')

    # Create 'backup_schedule' table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS backup_schedule (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        time TEXT NOT NULL
    )
    ''')

    # Insert default backup time if it doesn't exist
    cursor.execute('''
    INSERT INTO backup_schedule (id, time)
    SELECT 1, '02:00'
    WHERE NOT EXISTS(SELECT 1 FROM backup_schedule WHERE id = 1);
    ''')

    print("Database and tables created successfully")

    # Commit changes and close the connection
    conn.commit()
    conn.close()

if __name__ == '__main__':
    create_database()

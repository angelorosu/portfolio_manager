import sqlite3

def create_database():
    db_path = "watchlist.db"
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS watchlist (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            stock_symbol TEXT NOT NULL UNIQUE
        )
    ''')

    connection.commit()
    connection.close()
    print("Database and table created successfully.")

if __name__ == "__main__":
    create_database()



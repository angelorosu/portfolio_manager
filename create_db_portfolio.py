import sqlite3

def create_db_portfolio():
    db_path = "portfolio.db"
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    # Correctly execute the SQL statement
    cursor.execute('''
                        CREATE TABLE IF NOT EXISTS portfolio (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            stock_symbol TEXT NOT NULL,
                            positions REAL NOT NULL,
                            entry_price REAL NOT NULL,
                            entry_date TEXT NOT NULL
                        )
                   ''')
    
    connection.commit()
    connection.close() 
    print("Database and table created successfully.")

if __name__ == "__main__":
    create_db_portfolio()


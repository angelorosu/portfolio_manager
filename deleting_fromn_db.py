import sqlite3

def pop_stock_symbol(symbol):
    # Step 1: Connect to the database
    conn = sqlite3.connect('portfolio.db')
    cursor = conn.cursor()

    try:
        # Step 2: Retrieve the row with the specified stock_symbol
        cursor.execute("SELECT * FROM portfolio WHERE stock_symbol = ?", (symbol,))
        row = cursor.fetchone()

        if row:
            print("Retrieved row:", row)
            
            # Step 3: Delete the row from the database
            cursor.execute("DELETE FROM portfolio WHERE stock_symbol = ?", (symbol,))
            conn.commit()
            print(f"Stock symbol '{symbol}' has been deleted from the database.")

        else:
            print(f"No record found with stock_symbol = '{symbol}'")

    except sqlite3.Error as e:
        print("An error occurred:", e)

    finally:
        # Step 4: Close the connection
        conn.close()

# Example usage
pop_stock_symbol("aas")

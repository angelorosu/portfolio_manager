import sqlite3
import yfinance as yf

class DatabaseManager:
    def __init__(self, db_path):
        self.db_path = db_path

    def execute_query(self, query, params=()):
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()
        cursor.execute(query, params)
        connection.commit()
        connection.close()

    def fetch_all(self, query, params=()):
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()
        cursor.execute(query, params)
        result = cursor.fetchall()
        connection.close()
        return result

class StockDataFetcher:
    @staticmethod
    def fetch_stock_data(ticker):
        prices = yf.download(ticker, period='5d', interval='1d')
        live_price = prices['Close'][-1]
        yest_close = prices['Close'][-2]
        perc_change = (live_price - yest_close) / yest_close
        return live_price, yest_close, perc_change

class Portfolio:
    def __init__(self, db_manager):
        self.db_manager = db_manager
        self.portfolio = self.load_portfolio_from_db()

    def load_portfolio_from_db(self):
        return self.db_manager.fetch_all('SELECT stock_symbol, positions, entry_price, entry_date FROM portfolio')
    
    def add_port_stock(self, ticker, positions, entry_price, entry_date):
        try:
            # Ensure that positions and entry_price are floats
            positions = float(positions)
            entry_price = float(entry_price)

            # Check if the stock already exists in the portfolio
            existing_stock = self.db_manager.fetch_all(
                'SELECT positions, entry_price FROM portfolio WHERE stock_symbol = ?', (ticker,)
            )
            
            if existing_stock:
                print(f"Existing stock found: {existing_stock}")

                # Retrieve positions and entry price from existing stock
                existing_positions = existing_stock[0][0]
                existing_entry_price = existing_stock[0][1]


                # Convert to float if necessary
                existing_positions = float(existing_positions)
                existing_entry_price = float(existing_entry_price)

                # Calculate the new total positions and new average entry price
                total_positions = positions + existing_positions
                new_entry_price = ((existing_positions * existing_entry_price) + (positions * entry_price)) / total_positions


                # Update the existing record
                self.db_manager.execute_query(
                    'UPDATE portfolio SET positions = ?, entry_price = ?, entry_date = ? WHERE stock_symbol = ?',
                    (total_positions, new_entry_price, entry_date, ticker)
                )
                print('Stock updated successfully')

            else:
                
                # Insert new stock entry into the portfolio
                self.db_manager.execute_query(
                    'INSERT INTO portfolio (stock_symbol, positions, entry_price, entry_date) VALUES (?, ?, ?, ?)',
                    (ticker, positions, entry_price, entry_date)
                )
                print('New stock added successfully')

            # Reload the portfolio from the database
            self.portfolio = self.load_portfolio_from_db()

        except Exception as e:
            print(f"An error occurred while adding stock to the portfolio: {e}")


    def remove_stock(self, ticker):
        self.db_manager.execute_query('DELETE FROM portfolio WHERE stock_symbol = ?', (ticker,))
        self.portfolio = self.load_portfolio_from_db()

    def get_portfolio_data(self):
        port_live_data = []
        for record in self.portfolio:
            ticker, positions, entry_price, entry_date = record
            live_price, yest_close, perc_change = StockDataFetcher.fetch_stock_data(ticker)

            daily_pl = positions * yest_close * perc_change
            unrealised_pl = (live_price * positions) - (entry_price * positions)

            port_data = {
                'Ticker': ticker,
                'Price': live_price,
                'Positions': positions,
                'Change %': perc_change,
                'Daily P/L': daily_pl,
                'Unrealised P/L': unrealised_pl,
                'Entry Price': entry_price
            }

            port_live_data.append(port_data)

        return port_live_data


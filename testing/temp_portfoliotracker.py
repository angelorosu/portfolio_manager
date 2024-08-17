import yfinance as yf
import sqlite3

class PortfolioTracker:
    def __init__(self):
        self.db_path = "portfolio.db"
        self.portfolio = self.load_portfolio_from_db()

    def load_portfolio_from_db(self):
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()
        
        # Fetch all records from the portfolio table
        cursor.execute('SELECT stock_symbol, positions, entry_price, entry_date FROM portfolio')
        portfolio = cursor.fetchall()
        
        connection.close()
        return portfolio

    def add_to_portfolio_db(self, ticker, positions, entry_price, entry_date):
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()

        # Insert the data into the portfolio table
        cursor.execute('''
            INSERT OR IGNORE INTO portfolio (stock_symbol, positions, entry_price, entry_date)
            VALUES (?, ?, ?, ?)
        ''', (ticker, positions, entry_price, entry_date))

        connection.commit()
        connection.close()
        print(f"Added {ticker} to the portfolio.")

    def remove_from_portfolio(self, ticker):
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()

        # Remove the stock from the portfolio
        cursor.execute('DELETE FROM portfolio WHERE stock_symbol = ?', (ticker,))

        connection.commit()
        connection.close()
        print(f"Removed {ticker} from the portfolio.")

    def portfolio_data(self):
        port_live_data = []

        for record in self.portfolio:
            ticker, positions, entry_price, entry_date = record
            prices = yf.download(ticker, period='5d', interval='1d')
            live_price = prices['Close'][-1]
            yest_close = prices['Close'][-2]
            perc_change = (live_price - yest_close) / yest_close

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

        print(port_live_data)
        return port_live_data

# Example usage
tracker = PortfolioTracker()
tracker.add_to_portfolio_db('AAPL', 10, 150.00, '2023-01-15')
tracker.add_to_portfolio_db('TSLA', 5, 700.00, '2023-02-20')
tracker.add_to_portfolio_db('META',20, 50.00, '2023-03-25')
tracker.portfolio_data()

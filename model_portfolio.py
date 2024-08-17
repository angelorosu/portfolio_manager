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

    def add_stock(self, ticker, positions, entry_price, entry_date):
        self.db_manager.execute_query(
            'INSERT OR IGNORE INTO portfolio (stock_symbol, positions, entry_price, entry_date) VALUES (?, ?, ?, ?)',
            (ticker, positions, entry_price, entry_date)
        )
        self.portfolio = self.load_portfolio_from_db()

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


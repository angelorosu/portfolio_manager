#Angelo Rosu angelo.rosu2001@gmail.com
#Sameer Farooq sameerf2001@gmail.com

import yfinance as yf

import pandas as pd

import matplotlib.pyplot as plt

import sqlite3
from matplotlib.figure import Figure

class Watchlist:
    def __init__(self):
        self.db_path = "watchlist.db"
        self.stocks = self.load_watchlist_from_db()
        self.stock_live_data = []


    def add_stock(self, ticker):
        if ticker not in self.stocks:
            self.stocks.append(ticker)
            self.save_watchlist_to_db()
        
        

    def remove_stock(self, ticker):
        if ticker in self.stocks:
            self.stocks.remove(ticker)
            self.remove_stock_from_db(ticker)
            self.remove_stock_live_data(ticker)


    def get_current_price(self, ticker):
        try:
            data = yf.download(ticker, period='1d', interval='1m')
            if not data.empty and 'Close' in data.columns:
                return data['Close'].iloc[-1]
            else:
                print(f"Data for {ticker} is empty or missing 'Close' column.")
                return 0.0
        except Exception as e:
            print(f"Error fetching price for {ticker}: {e}")
            return 0.0

    def fetch_live_data(self):
        # Fetch live data for all stocks in the watchlist
        self.stock_live_data = []

        for ticker in self.stocks:

            stock = yf.Ticker(ticker)
            price = self.get_current_price(ticker)
            info = stock.info

            market_cap = info.get('marketCap', 'N/A')
            volume = info.get('volume', 'N/A')
            pe_0 = info.get('trailingPE', 'N/A') #relook at pe0 and pe1
            pe_1 = info.get('trailingPE', 'N/A')  
            beta = info.get('beta', 'N/A')

            # Fetch previous close price for percentage change calculation
            data = yf.download(ticker, period='5d', interval='1d')
            if len(data) > 1:
                close_price = data['Close'][-2]
                change_percentage = ((price - close_price) / close_price) * 100
            else:
                close_price = 0
                change_percentage = 0

            stock_data = {
                'Ticker': ticker,
                'Price': price,
                'Market Cap': market_cap,
                'Volume': volume,
                'PE0 Ratio': pe_0,
                'PE1 Ratio': pe_1,
                'Beta': beta,
                'Change %': change_percentage
            }

            self.stock_live_data.append(stock_data)
            

    def present_live_data(self):
        # Present live data for all stocks in a readable format
    
        live_data = pd.DataFrame(self.stock_live_data)
        

    
    
    def graph(self,ticker):
        hist_data = yf.download(ticker, period='2y', interval='1d')
        fig = Figure(figsize=(10, 6))
        ax = fig.add_subplot(111)
        ax.plot(hist_data.index, hist_data['Close'], label='Closing Price', color='blue')
        ax.set_title(f'{ticker} Closing Price')
        ax.set_xlabel('Date')
        ax.set_ylabel('Price')
        ax.legend()
        ax.grid(True)
        return fig


    def load_watchlist_from_db(self):
        # Connect to the database
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()

        # Example query to fetch the watchlist
        cursor.execute("SELECT stock_symbol FROM watchlist")
        rows = cursor.fetchall()

        # Convert rows to a list of stock symbols
        watchlist = [row[0] for row in rows]

        # Close the database connection
        connection.close()

        return watchlist
    
    def save_watchlist_to_db(self):
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()

        cursor.executemany("INSERT OR IGNORE INTO watchlist (stock_symbol) VALUES (?)", [(ticker,) for ticker in self.stocks])

        connection.commit()
        connection.close()

    def remove_stock_from_db(self, ticker):
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()

        cursor.execute("DELETE FROM watchlist WHERE stock_symbol = ?", (ticker,))

        connection.commit()
        connection.close()

    def remove_stock_live_data(self, ticker):
        # Filter out the stock data that doesn't match the ticker
        self.stock_live_data = [data for data in self.stock_live_data if data['Ticker'] != ticker]

class Portfolio_Tracker:
    # Placeholder class for tracking a portfolio, functionality to be added

    pass



class Comparison:
    # Placeholder class for comparing stocks, functionality to be added
    pass


# Example usage
if __name__ == "__main__":
    watchlist = Watchlist()
    watchlist.create_database()
    watchlist.add_stock('AAPL')
    watchlist.add_stock('MSFT')
    watchlist.add_stock('GOOGL')
    watchlist.add_stock('META')
    watchlist.add_stock('FOUR')

    watchlist.fetch_live_data()
    watchlist.present_live_data()
    watchlist.graph('AAPL')
    

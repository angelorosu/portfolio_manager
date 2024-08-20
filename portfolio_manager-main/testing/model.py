import yfinance as yf
import time as time
from alpha_vantage.timeseries import TimeSeries



class Watchlist:
    def __init__(self,stocks,data):

        self.stocks = stocks
        self.data = data
        self.ticker = ticker

        self.stock_live_data =[]

    def get_current_price(self):
        try:
            #print(f"Fetching price for ticker: {ticker}")  # Debugging line
            self.data = yf.download(ticker, period='1d', interval='1m')
            #print(f"Fetched data: {data}")  # Debugging line
            if not self.data.empty and 'Close' in self.data.columns:
                return self.data['Close'].iloc[-1]
            else:
                print(f"Data is empty or missing 'Close' column")  # Debugging line
            return 0.0
        except Exception as e:
            print(f"Error fetching price for {ticker}: {e}")  # Debugging line
            return 0.0
    
    def fetch_live_data(self,stock,ticker):
        # Fetch Price, Market Cap, Volume, Next EPS date, P/E,Beta,
        self.stocks = yf.Ticker(ticker)
   
        #   Get stock information
        info = stock.info
        data = yf.download(ticker, period='5d',interval='1d')

        for ticker in self.stocks:
            price = self.get_current_price(ticker)
            market_cap = info.get('marketCap', 'N/A')
            volume = info.get('volume', 'N/A')
            pe_ratio = info.get('trailingPE', 'N/A')
            beta = info.get('beta', 'N/A')
            close_price = data['Close'][-2]
            change_percentage = ((price-close_price)/close_price)
            print(price)
            
    fetch_live_data()
        

    def present_live_data(self):
        # Present live data
        pass

    def add_stock(self, stock):
        self.stocks.append(stock)

    def remove_stock(self, stock):
        self.stocks.remove(stock)


class Portfolio_Tracker:
    pass



class Comparison:
    pass
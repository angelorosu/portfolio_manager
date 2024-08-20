import yfinance as yf
import matplotlib.pyplot as plt

class Comparison:
    def __init__(self):
        pass
    
    def get_adj_close_for_ticker(self, ticker):
        adj_close = yf.download(ticker, period='2y', interval='1d')['Adj Close']
        return adj_close

    def compare_tickers_spread(self, ticker1, ticker2):
        adj_close1 = self.get_adj_close_for_ticker(ticker1)
        adj_close2 = self.get_adj_close_for_ticker(ticker2)
        spread = adj_close1 - adj_close2
        return spread

    def compare_tickers_ratio(self, ticker1, ticker2):
        adj_close1 = self.get_adj_close_for_ticker(ticker1)
        adj_close2 = self.get_adj_close_for_ticker(ticker2)
        ratio = adj_close1 / adj_close2
        return ratio

    def graph(self, ticker_info, title='Spread/Ratio Over Time'):
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(ticker_info.index, ticker_info, label=title, color='blue')
        ax.set_title(title)
        ax.set_xlabel('Date')
        ax.set_ylabel('Value')
        ax.legend()
        ax.grid(True)
        plt.show()


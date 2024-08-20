# controller.py

from model_v2 import Watchlist
from view import WatchlistView
from model_portfolio import Portfolio
from view_portfolio import PortfolioView
from model_portfolio import DatabaseManager
from model_comparison import Comparison
from view_comparison import ComparisonView


class WatchlistController:
    def __init__(self, root):
        self.model = Watchlist()
        self.view = WatchlistView(root, self)
        self.view.pack()
        print('WatchlistController initialized')
        self.fetch_and_update_data()
        

    def add_stock(self, stock):
        if stock not in self.model.stocks:
            self.model.add_stock(stock)
            self.fetch_and_update_data()

    def remove_stock(self, stock):
        self.model.remove_stock(stock)
        self.view.update_view(self.model.stock_live_data)

    
    def fetch_and_update_data(self):
        
        self.model.fetch_live_data() # method from model to fetch live data
        self.view.update_view(self.model.stock_live_data)  # method in view which is updated from model stock lived data

    def get_watchlist(self):
        return self.model.stocks()
    
        
    def plot_graph(self, ticker):
        fig = self.model.graph(ticker)
        self.view.display_plot(fig)

    
    


class PortfolioController:
    def __init__(self, root):
        self.dbmanger = DatabaseManager('portfolio.db')
        self.model = Portfolio(self.dbmanger)
        self.view = PortfolioView(root, self)
          # Ensure the controller is passed correctly
        self.view.pack()
        print('PortfolioController initialized')
        self.view.port_update_view(self.model.get_portfolio_data())
       
    
    def add_record_to_portfolio(self, ticker, positions, entry_price, entry_date):
        self.model.add_port_stock(ticker, positions, entry_price, entry_date)
        self.view.port_update_view(self.model.get_portfolio_data())

    def remove_record_from_portfolio(self, ticker):
        self.model.remove_stock(ticker)
        self.view.port_update_view(self.model.get_portfolio_data())


class ComparisonController:
    def __init__(self,root):
        self.model = Comparison()
        self.view = ComparisonView(root, self)
        self.view.pack()
        print('ComparisonController initialized')
        self.view.update_view(self.model.get_comparison_data())
        
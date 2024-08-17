# controller.py

from model_v2 import Watchlist
from view import WatchlistView

class WatchlistController:
    def __init__(self, root):
        self.model = Watchlist()
        self.view = WatchlistView(root, self)
        self.view.pack()
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
    pass
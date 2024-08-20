import tkinter as tk
from controller import WatchlistController
from controller import PortfolioController
from view import *
from starting_screen_view import StartingScreen
from view_portfolio import PortfolioView
from view_comparison import ComparisonView
from controller import ComparisonController

def start_watchlist():
    # Create the root window if it doesn't exist yet
    if not hasattr(start_watchlist, 'root'):
        start_watchlist.root = tk.Tk()
        start_watchlist.root.title("Watchlist App")
        start_watchlist.root.geometry("1000x800")  # Initial window size
        # Create the controller and pass it to the Application
        controller = WatchlistController(start_watchlist.root)
        #app = controller(controller)
        #app.pack(fill=tk.BOTH, expand=True)

    # Show the main application window and hide the starting screen
    start_watchlist.root.deiconify()
    start_watchlist.root.mainloop()

def start_portfolio():

    if not hasattr(start_portfolio, 'root'):
        start_portfolio.root = tk.Tk()
        start_portfolio.root.title("Portfolio App")
        start_portfolio.root.geometry("1280x720")
        print("Size has been set")
        controller = PortfolioController(start_portfolio.root)
    start_portfolio.root.deiconify()
    start_portfolio.root.mainloop()

def start_comparison():

    if not hasattr(start_comparison, 'root'):
        start_comparison.root = tk.Tk()
        start_comparison.root.title("Comparison App")
        start_comparison.root.geometry("1280x720")
        controller = ComparisonController(start_comparison.root)
    start_comparison.root.deiconify()
    start_comparison.root.mainloop()
    

def start_starting_screen():
    # Create the root window and hide it initially
    root = tk.Tk()
    root.withdraw()  # Hide the root window initially

    # Create and show the starting screen
    starting_screen = StartingScreen(root, start_watchlist, start_portfolio, start_comparison) 
    
    starting_screen.mainloop()
    

if __name__ == "__main__":
    start_starting_screen()

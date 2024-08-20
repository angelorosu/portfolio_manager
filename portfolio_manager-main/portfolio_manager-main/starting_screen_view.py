import tkinter as tk

class StartingScreen(tk.Toplevel):
    def __init__(self, parent, on_start, on_open_portfolio,on_open_comparison):
        super().__init__(parent)
        self.title("Starting Screen")
        self.geometry("540x420")
        self.on_start = on_start
        self.on_open_portfolio = on_open_portfolio
        self.on_open_comparison = on_open_comparison
        # Displaying a label
        self.label = tk.Label(self, text="Welcome to the Stocks Portfolio Manager", font=("Helvetica", 16))
        self.label.pack(pady=20)

        # Button to open the watchlist
        self.start_button = tk.Button(self, text="Open Watchlist", command=self.open_main_application)
        self.portfolio_button = tk.Button(self, text="Open Portfolio", command=self.open_portfolio)
        self.comparison_button = tk.Button(self, text="Open Comparison", command=self.open_comparison)
        self.start_button.pack(pady=20)
        self.portfolio_button.pack(pady=20)
        self.comparison_button.pack(pady=20)

    def open_main_application(self):
        self.destroy()  # Close the starting screen
        self.on_start()  # Call the function to start the main application (watchlist)

    def open_portfolio(self):
        self.destroy()  # Close the starting screen
        self.on_open_portfolio()  # Call the function to open the portfolio

    def open_comparison(self):
        self.destroy()
        self.on_open_comparison()

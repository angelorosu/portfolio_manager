import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import tkinter as tk
from tkinter import ttk


class WatchlistView(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Label
        self.label = tk.Label(self, text="Watchlist", font=("Helvetica", 18))
        self.label.grid(row=0, column=0, columnspan=2, pady=10, sticky="ew")

        # Table for stock data
        self.tree = ttk.Treeview(self, columns=(
            'Ticker', 'Price', 'Market Cap', 'Volume',
            'PE0 Ratio', 'PE1 Ratio', 'Beta', 'Change %'), show='headings')

        columns = [
            ('Ticker', 'Ticker'),
            ('Price', 'Price'),
            ('Market Cap', 'Market Cap'),
            ('Volume', 'Volume'),
            ('PE0 Ratio', 'PE0 Ratio'),
            ('PE1 Ratio', 'PE1 Ratio'),
            ('Beta', 'Beta'),
            ('Change %', 'Change %')
        ]

        for col, heading in columns:
            self.tree.heading(col, text=heading)
            self.tree.column(col, anchor=tk.CENTER, width=120)

        self.tree.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

        # Entry and Buttons
        self.add_ticker_entry = tk.Entry(self)
        self.add_ticker_entry.grid(row=2, column=0, padx=10, pady=5, sticky="ew")

        self.add_button = tk.Button(self, text="Add Stock", command=lambda: self.controller.add_stock(self.add_ticker_entry.get()))
        self.add_button.grid(row=3, column=0, padx=10, pady=5, sticky="ew")

        self.remove_button = tk.Button(self, text="Remove Stock", command=lambda: self.controller.remove_stock(self.add_ticker_entry.get()))
        self.remove_button.grid(row=4, column=0, padx=10, pady=5, sticky="ew")

        self.graph_button = tk.Button(self, text="Graph", command=lambda: self.controller.plot_graph(self.add_ticker_entry.get()))
        self.graph_button.grid(row=5, column=0, padx=10, pady=5, sticky="ew")

        # Frame for plot
        self.plot_frame = tk.Frame(self, borderwidth=2, relief='solid')
        self.plot_frame.grid(row=3, column=1, rowspan=6, padx=10, pady=10, sticky="nsew")

        # Configure row/column weights
        self.grid_rowconfigure(1, weight=2)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=3)

    def display_plot(self, fig):
        # Clear any existing plot
        for widget in self.plot_frame.winfo_children():
            widget.destroy()

        # Embed the matplotlib figure in Tkinter
        canvas = FigureCanvasTkAgg(fig, master=self.plot_frame)
        canvas.draw()

        # Add navigation toolbar
        toolbar = NavigationToolbar2Tk(canvas, self.plot_frame)
        toolbar.update()
        toolbar.pack(side=tk.TOP, fill=tk.X)

        # Pack the canvas
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def update_view(self, stock_live_data):
        print("Updating View with data", stock_live_data)

        # Clear the existing rows in the Treeview
        self.tree.delete(*self.tree.get_children())

        # Maintain a set of tickers already added to avoid duplicates
        existing_tickers = set()

        # Insert new rows with updated stock data
        for stock in stock_live_data:
            if isinstance(stock, dict):
                ticker = stock.get('Ticker', 'N/A')

                if ticker not in existing_tickers:
                    price = "{:.2f}".format(stock.get('Price', 0.0)) if stock.get('Price') is not None else 'N/A'
                    market_cap = "{:,}".format(stock.get('Market Cap', 'N/A')) if stock.get('Market Cap') != 'N/A' else 'N/A'
                    volume = "{:,}".format(stock.get('Volume', 'N/A')) if stock.get('Volume') != 'N/A' else 'N/A'
                    change_percent = "{:.2f}".format(stock.get('Change %', 0.0)) if stock.get('Change %') is not None else 'N/A'

                    self.tree.insert("", tk.END, values=(
                        ticker, 
                        price, 
                        market_cap, 
                        volume, 
                        stock.get('PE0 Ratio', 'N/A'), 
                        stock.get('PE1 Ratio', 'N/A'), 
                        stock.get('Beta', 'N/A'), 
                        change_percent
                    ))
                    existing_tickers.add(ticker)
            else:
                print("Unexpected format:", stock)


class StartingScreen(tk.Toplevel):
    def __init__(self, parent, on_start):
        super().__init__(parent)
        self.title("Starting Screen")
        self.geometry("300x200")
        self.on_start = on_start

        # Displaying a label
        self.label = tk.Label(self, text="Welcome to the Stocks Portfolio Manager", font=("Helvetica", 16))
        self.label.pack(pady=20)

        # Button to open the main application
        self.start_button = tk.Button(self, text="Open Watchlist", command=self.open_main_application)
        self.start_button.pack(pady=20)

    def open_main_application(self):
        self.destroy()  # Close the starting screen
        self.on_start()  # Call the function to start the main application


class Application(tk.Tk):
    def __init__(self, controller):
        super().__init__()
        self.title("Watchlist App")
        self.geometry("800x600")  # Initial window size

        # Create and display the WatchlistView frame
        self.controller = controller
        self.controller.fetch_and_update_data()
        self.watchlist_view = self.controller.view
        self.watchlist_view.pack(fill=tk.BOTH, expand=True)

        # Fullscreen toggle
        self.attributes('-fullscreen', False)
        self.bind('<F11>', self.toggle_fullscreen)  # Bind F11 key to toggle fullscreen
        self.bind('<Escape>', self.disable_fullscreen)  # Bind Escape key to exit fullscreen

    def toggle_fullscreen(self, event=None):
        self.attributes('-fullscreen', True)
        return "break"

    def disable_fullscreen(self, event=None):
        self.attributes('-fullscreen', False)
        return "break"

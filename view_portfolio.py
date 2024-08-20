import tkinter as tk
from tkinter import ttk
from functools import partial


class PortfolioView(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        self.label = tk.Label(self, text="Portfolio Screen", font=("Helvetica", 16))
        self.label.grid(row=0, column=0, columnspan=4, pady=10, sticky="ew")

        # Labels and Entry widgets
        tk.Label(self, text="Ticker:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.add_to_portfolio_ticker = tk.Entry(self)
        self.add_to_portfolio_ticker.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

        tk.Label(self, text="Position:").grid(row=2, column=0, padx=10, pady=5, sticky="e")
        self.add_to_portfolio_position = tk.Entry(self)
        self.add_to_portfolio_position.grid(row=2, column=1, padx=10, pady=5, sticky="ew")

        tk.Label(self, text="Entry Price:").grid(row=3, column=0, padx=10, pady=5, sticky="e")
        self.add_to_portfolio_entry_price = tk.Entry(self)
        self.add_to_portfolio_entry_price.grid(row=3, column=1, padx=10, pady=5, sticky="ew")

        tk.Label(self, text="Entry Date:").grid(row=4, column=0, padx=10, pady=5, sticky="e")
        self.add_to_portfolio_entry_date = tk.Entry(self)
        self.add_to_portfolio_entry_date.grid(row=4, column=1, padx=10, pady=5, sticky="ew")

        # Button to record the trade to portfolio
        self.add_to_portfolio_button = tk.Button(
            self, 
            text="Add to Portfolio", 
            command=self.on_add_to_portfolio
        )
        self.add_to_portfolio_button.grid(row=5, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

        #button to delete record
        self.delete_record_button = tk.Button(
            self,
            text="Delete Record",
            command=self.on_delete_record
        )
        self.delete_record_button.grid(row=6, column=0, columnspan=2, padx=10, pady=10, sticky="ew")



        self.port_tree = ttk.Treeview(self, columns=(
            'Ticker', 'Price', 'Positions', 'Change %', 
            'Daily P/L', 'Unrealised P/L', 'Entry Price'
        ), show='headings')

        columns = [
            ('Ticker', 'Ticker'),
            ('Price', 'Price'),
            ('Positions', 'Positions'),
            ('Change %', 'Change %'),
            ('Daily P/L', 'Daily P/L'),
            ('Unrealised P/L', 'Unrealised P/L'), 
            ('Entry Price', 'Entry Price')
        ]

        for col, heading in columns:
            self.port_tree.heading(col, text=heading)
            self.port_tree.column(col, anchor=tk.CENTER, width=120)

        self.port_tree.grid(row=1, column=2, columnspan=1, rowspan=4, padx=10, pady=10, sticky="ew")

    def on_delete_record(self):
        print('button clicked, deleting record')
        ticker = self.add_to_portfolio_ticker.get().strip()
        if not ticker:
            print("Error: Ticker field must be filled.")
            return

        self.controller.remove_record_from_portfolio(ticker)


    def on_add_to_portfolio(self):

        print('button clicked, adding to portfolio')
        ticker = self.add_to_portfolio_ticker.get().strip()
        positions = self.add_to_portfolio_position.get().strip()
        entry_price = self.add_to_portfolio_entry_price.get().strip()
        entry_date = self.add_to_portfolio_entry_date.get().strip()
        if not ticker or not positions or not entry_price or not entry_date:
            print("Error: All fields must be filled.")
            return

        try:
            positions = int(positions)  # Convert to integer
            # entry_date remains a string, assuming it's in a valid date format
        except ValueError as e:
            print(f"Error: Invalid input - {e}")
            return

        # Call the controller's method with parameters
        self.controller.add_record_to_portfolio(ticker, positions, entry_price, entry_date)


    def port_update_view(self, port_live_data):
        print("Updating View with data", port_live_data)

        # Clear the existing rows in the Treeview
        self.port_tree.delete(*self.port_tree.get_children())

        # Maintain a set of tickers already added to avoid duplicates
        existing_tickers = set()

        # Insert new rows with updated stock data
        for stock in port_live_data:
            if isinstance(stock, dict):
                ticker = stock.get('Ticker', 'N/A')

                if ticker not in existing_tickers:
                    price = "{:.2f}".format(stock.get('Price', 0.0)) if stock.get('Price') is not None else 'N/A'
                    positions = stock.get('Positions', 'N/A')
                    change_percent = "{:.2f}".format(stock.get('Change %', 0.0)) if stock.get('Change %') is not None else 'N/A'
                    daily_pl = "{:.2f}".format(stock.get('Daily P/L', 0.0)) if stock.get('Daily P/L') is not None else 'N/A'
                    unrealized_pl = "{:.2f}".format(stock.get('Unrealised P/L', 0.0)) if stock.get('Unrealised P/L') is not None else 'N/A'
                    entry_price = "{:.2f}".format(stock.get('Entry Price', 0.0)) if stock.get('Entry Price') is not None else 'N/A'

                    self.port_tree.insert("", tk.END, values=(
                        ticker, 
                        price, 
                        positions, 
                        change_percent, 
                        daily_pl, 
                        unrealized_pl, 
                        entry_price
                    ))
                    existing_tickers.add(ticker)
            else:
                print("Unexpected format:", stock)

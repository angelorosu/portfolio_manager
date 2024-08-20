import tkinter as tk
from tkinter import ttk


class ComparisonView(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.label = tk.Label(self, text="Comparison Screen", font=("Helvetica", 16))
        self.label.grid(row=0, column=0, columnspan=4, pady=10, sticky="ew")

        # Labels and Entry widgets
        tk.Label(self, text = "Ticker 1").grid(row =1,column=0,padx=10,pady=5,sticky="e")
        self.add_first_ticker = tk.Entry(self)
        self.add_first_ticker.grid(row = 1,column=1,padx=10,pady=5,sticky="ew")

        tk.Label(self, text = "Ticker 2").grid(row =2,column=0,padx=10,pady=5,sticky="e")
        self.add_second_ticker = tk.Entry(self)
        self.add_second_ticker.grid(row=2,column=1,padx=10,pady=5,sticky="ew")

        tk.Label(self, text = "Spread").grid(row =3,column=0,padx=10,pady=5,sticky="e")
        self.plot_frame_spread = tk.Frame(self, borderwidth=2, relief='solid')
        self.plot_frame_spread.grid(row=3, column=1, rowspan=5,columnspan=5, padx=10, pady=10, sticky="nsew")

        tk.Label(self, text = "Ratio").grid(row =9,column=6,padx=10,pady=5,sticky="e")
        self.plot_frame_spread = tk.Frame(self, borderwidth=2, relief='solid')
        self.plot_frame_spread.grid(row=3, column=1, rowspan=5,columnspan=5, padx=10, pady=10, sticky="nsew")

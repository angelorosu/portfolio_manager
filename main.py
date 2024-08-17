import tkinter as tk
from controller import WatchlistController
from view import StartingScreen, Application

def start_main_application():
    controller = WatchlistController(tk.Tk())  # Create a new root for the application
    app = Application(controller)
    app.mainloop()

def start_application():
    root = tk.Tk()  # Create the root window
    root.withdraw()  # Hide the root window
    
    # Create and show the starting screen
    starting_screen = StartingScreen(root, start_main_application)
    root.mainloop()



if __name__ == "__main__":
    start_application()
    

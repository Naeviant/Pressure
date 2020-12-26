import tkinter as tk
from functools import partial
from os import path

from game import Game
from scoreboard import Scoreboard
from help import Help
from settings import Settings


# Main menu class
class MainMenu:
    # Build window
    def __init__(self):
        # Configures window
        self.window = tk.Tk()
        self.window.protocol("WM_DELETE_WINDOW", self.prevent)
        self.window.resizable(False, False)
        self.window.title("Pressure: Launchpad")

        # Display new and load game buttons
        tk.Label(self.window, text="Pressure", font=("Arial", 25)).grid(
            row=0, column=0, columnspan=2, pady=3)
        tk.Button(self.window, text="New Game", command=partial(
            self.surrender, "new"), width=12, height=2).grid(
                row=1, column=0, padx=10, pady=5)
        self.load_button = tk.Button(self.window, text="Load Game",
                                     command=partial(self.surrender, "load"),
                                     width=12, height=2)
        self.load_button.grid(row=1, column=1, padx=10, pady=5)

        # Disable load button if game not saved
        if not path.exists("save.json"):
            self.load_button.config(state="disabled")

        # Display other buttons
        tk.Button(self.window, text="Scoreboard", command=partial(
            self.surrender, "scoreboard"), width=12, height=2).grid(
                row=2, column=0, padx=10, pady=5)
        tk.Button(self.window, text="How to Play", command=partial(
            self.surrender, "help"), width=12, height=2).grid(
                row=2, column=1, padx=10, pady=5)
        tk.Button(self.window, text="Settings", command=partial(
            self.surrender, "settings"), width=12, height=2).grid(
                row=3, column=0, padx=10, pady=5)
        tk.Button(self.window, text="Exit Game", command=partial(
            self.die), width=12, height=2).grid(row=3, column=1,
                                                padx=10, pady=5)

        # Display window
        self.window.mainloop()

    # Open new window and hide
    def surrender(self, code):
        # Hides menu
        self.window.withdraw()

        # Open new window
        if code == "new":
            Game(False)
        elif code == "load":
            Game(True)
        elif code == "scoreboard":
            Scoreboard()
        elif code == "help":
            Help()
        elif code == "settings":
            Settings()

        # Enable or disable load game button if game saved
        if path.exists("save.json"):
            self.load_button.config(state="normal")
        else:
            self.load_button.config(state="disabled")

        # Hides menu
        self.window.deiconify()

    # Dummy function used to disable close button
    def prevent(self):
        pass

    # Destroy window
    def die(self):
        # Close window
        self.window.destroy()


# Warn users who execute this file directly
if __name__ == "__main__":
    print("You have executed the wrong file. Please read the README, "
          "and then execute the pressure.py file.")

import tkinter as tk
from functools import partial
from time import localtime, strftime
import json


# Scoreboard class
class Scoreboard:
    # Build window
    def __init__(self):
        # Configures window
        self.window = tk.Tk()
        self.window.protocol("WM_DELETE_WINDOW", self.prevent)
        self.window.resizable(False, False)
        self.window.title("Scoreboard")

        # Display title of window
        tk.Label(self.window, text="Scoreboard", font=("Arial", 25)).grid(
            row=0, column=0, columnspan=5, pady=10)

        # Get scoreboard data
        raw_data = open("scoreboard.json")
        scoreboard = json.load(raw_data)
        scoreboard = sorted(scoreboard, key=lambda x: x["score"])
        scoreboard.reverse()

        # Generate scoreboard data
        tk.Label(self.window, text="#", font=("Arial", 14, "bold")).grid(
            row=1, column=0, padx=(20, 10), pady=5)
        tk.Label(self.window, text="Name", font=("Arial", 14, "bold")).grid(
            row=1, column=1, padx=10, pady=5)
        tk.Label(self.window, text="Date Played", font=(
            "Arial", 14, "bold")).grid(row=1, column=2, padx=10, pady=5)
        tk.Label(self.window, text="No. of Plates", font=(
            "Arial", 14, "bold")).grid(row=1, column=3, padx=10, pady=5)
        tk.Label(self.window, text="Score", font=("Arial", 14, "bold")).grid(
            row=1, column=4, padx=(10, 20), pady=5)

        # Loop through data and displays row
        i = 2
        for player in scoreboard:
            tk.Label(self.window, text=i-1).grid(row=i,
                                                 column=0,
                                                 padx=(20, 10),
                                                 pady=5)
            tk.Label(self.window, text=player["name"]).grid(
                row=i, column=1, padx=10, pady=5)
            tk.Label(self.window, text=strftime(
                "%d/%m/%y", localtime(player["timestamp"]))).grid(row=i,
                                                                  column=2,
                                                                  padx=10,
                                                                  pady=5)
            tk.Label(self.window, text=player["plates"]).grid(
                row=i, column=3, padx=10, pady=5)
            tk.Label(self.window, text=player["score"]).grid(
                row=i, column=4, padx=(10, 20), pady=5)
            i += 1

        # Display menu button
        tk.Button(self.window, text="Main Menu", command=partial(
            self.die), width=24, height=2).grid(row=i, column=0, columnspan=5,
                                                pady=10)

        # Display window
        self.window.mainloop()

    # Dummy function used to disable close button
    def prevent(self):
        pass

    # Destroy window
    def die(self):
        # Quit and destroy used together allow the main menu to resume
        self.window.quit()
        self.window.destroy()


# Warn users who execute this file directly
if __name__ == "__main__":
    print("You have executed the wrong file. Please read the README, "
          "and then execute the pressure.py file.")

import tkinter as tk
from functools import partial
from time import time
import json


# Game over screen class
class GameOver:
    # Build window
    def __init__(self, score):
        # Configures window
        self.window = tk.Tk()
        self.window.protocol("WM_DELETE_WINDOW", self.prevent)
        self.window.resizable(False, False)
        self.window.title("Game Over")

        # Displays text on screen
        tk.Label(self.window, text="Game Over!", font=("Arial", 25)).grid(
            row=0, column=0, columnspan=2, padx=10, pady=5)
        tk.Label(self.window, text="Your score was " + str(score),
                 font=("Arial", 15)).grid(
            row=1, column=0, columnspan=2, padx=10, pady=5)

        tk.Label(self.window, text="Enter Your Name: ").grid(
            row=2, column=0, padx=(10, 5), pady=5)

        # Receive input from user
        self.name = tk.Text(self.window, height=1, width=12)
        self.name.grid(row=2, column=1, padx=(5, 10), pady=5)

        # Display save button
        self.save_button = tk.Button(
            self.window, text="Save to Leaderboard", width=24,
            height=2, command=partial(self.save, score))
        self.save_button.grid(row=3, column=0, columnspan=2,
                              padx=10, pady=5)

        # Display menu button
        tk.Button(self.window, text="Main Menu", width=24,
                  height=2,
                  command=partial(self.die)).grid(
            row=4, column=0, columnspan=2, padx=10, pady=5)

        # Display window
        self.window.mainloop()

    # Save to leaderboard
    def save(self, score):
        # Load file
        raw_data = open("scoreboard.json")
        scoreboard = json.load(raw_data)

        # Save to file
        scoreboard.append({
            "name": self.name.get("1.0", "end-1c"),
            "plates": (score // 3000) + 3,
            "timestamp": time(),
            "score": score
        })
        with open("scoreboard.json", "w") as output:
            json.dump(scoreboard, output)

        # Disable save button to prevent multiple entries being saved
        self.save_button.config(state="disabled")

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

import tkinter as tk
from functools import partial


# Instructions screen class
class Help:
    # Build window
    def __init__(self):
        # Configures window
        self.window = tk.Tk()
        self.window.protocol("WM_DELETE_WINDOW", self.prevent)
        self.window.resizable(False, False)
        self.window.geometry("600x500")
        self.window.title("How to Play")

        # Display header
        tk.Label(self.window, text="How to Play",
                 font=("Arial", 25)).pack(pady=10)

        # Generate instructions text
        line1 = "The game is simple. You play as a blue circle which " \
            "has to navigate around a maze-like area to keep pressure " \
            "plates active."
        line2 = "The pressure plates appear as coloured squares on the " \
            "area. Each pressure plate has a timeout period between 20 " \
            "and 40 seconds. Every time you cross over a pressure " \
            "plate, its timer resets to its full period. But when " \
            "you're not on it, it will slowly tick down."
        line3 = "When a pressure plate has 50% of its time left, it turns " \
            "yellow. When it has 25% of its time left, it turns orange. " \
            "When it has 10% of its time left, it turns red."
        line4 = "If any pressure plate stays red for too long and times " \
            "out, you lose."
        line5 = "The game will start with three pressure plates in " \
            "random locations. Every 30 seconds, a new plate " \
            "appears in a random location."

        # Display instructions
        tk.Label(self.window, text="Welcome to Pressure!").pack(pady=10)
        tk.Label(self.window, wraplength=590, text=line1).pack(pady=10)
        tk.Label(self.window, wraplength=590, text=line2).pack(pady=10)
        tk.Label(self.window, wraplength=590, text=line3).pack(pady=10)
        tk.Label(self.window, wraplength=590, text=line4).pack(pady=10)
        tk.Label(self.window, wraplength=590, text=line5).pack(pady=10)
        tk.Label(self.window, text="Good luck!").pack(pady=10)

        # Display main menu button
        tk.Button(self.window, text="Main Menu", command=partial(
            self.die), width=24, height=2).pack(pady=10)

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

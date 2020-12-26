import tkinter as tk
from functools import partial


# Pause menu class
class PauseMenu:
    # Build window
    def __init__(self, master):
        # Configures window
        self.window = tk.Tk()
        self.window.protocol("WM_DELETE_WINDOW", self.prevent)
        self.window.resizable(False, False)
        self.window.title("Pause")

        # Display paused text
        tk.Label(self.window, text="Paused", font=(
            "Arial", 25)).pack(padx=10, pady=5)

        # Display buttons
        tk.Button(self.window, text="Resume", width=12, height=2,
                  command=partial(self.die, "resume", master)).pack(
            padx=10, pady=5)
        tk.Button(self.window, text="Save Game", width=12, height=2,
                  command=partial(self.save, master)).pack(padx=10, pady=5)
        tk.Button(self.window, text="Main Menu", width=12, height=2,
                  command=partial(self.die, "menu", master)).pack(
            padx=10, pady=5)

        # Display window
        self.window.mainloop()

    # Save game
    def save(self, master):
        # Calls save() function from Game class
        master.save()

    # Dummy function used to disable close button
    def prevent(self):
        pass

    # Destroy window
    def die(self, code, master):
        # Destory Game instance if returning to main menu
        if code == "menu":
            master.die()

        # Quit and destroy used together allow the main menu to resume
        self.window.quit()
        self.window.destroy()


if __name__ == "__main__":
    print("You have executed the wrong file. Please read the README, "
          "and then execute the pressure.py file.")
